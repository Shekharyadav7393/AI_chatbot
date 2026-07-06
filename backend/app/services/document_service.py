import os
import uuid
from pathlib import Path
from typing import Any

import aiofiles
import pypdf
import docx2txt
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.database.session import async_session_maker
from app.embeddings.hf_embeddings import get_embedding_service
from app.models.document import DocumentStatus
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentListResponse, DocumentResponse
from app.utils.exceptions import DocumentProcessingError, NotFoundError, ValidationError
from app.utils.helpers import get_file_extension
from app.utils.logger import get_logger
from app.utils.validators import sanitize_filename, validate_file_size, validate_file_type
from app.vectorstore.chroma_store import ChromaVectorStore

settings = get_settings()
logger = get_logger(__name__)


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.doc_repo = DocumentRepository(db)

    async def upload_document(self, file: UploadFile, user_id: uuid.UUID) -> DocumentResponse:
        if not file.filename or not validate_file_type(file.filename):
            raise ValidationError("Unsupported file type. Allowed: PDF, DOCX, TXT")

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if not validate_file_size(file_size):
            limit_mb = settings.MAX_UPLOAD_SIZE // (1024 * 1024)
            raise ValidationError(f"File size exceeds {limit_mb}MB limit")

        user_dir = Path(settings.UPLOAD_DIR) / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        safe_filename = sanitize_filename(file.filename)
        file_path = user_dir / f"{uuid.uuid4()}_{safe_filename}"

        try:
            async with aiofiles.open(file_path, "wb") as out_file:
                while content := await file.read(1024 * 1024):
                    await out_file.write(content)
        except Exception as e:
            logger.error("Error saving file: %s", e)
            raise DocumentProcessingError("Failed to save file to disk") from e

        document = await self.doc_repo.create(
            {
                "filename": file.filename,
                "file_type": get_file_extension(file.filename)[1:],
                "file_path": str(file_path),
                "file_size": file_size,
                "uploaded_by": user_id,
                "status": DocumentStatus.processing,
            }
        )
        return DocumentResponse.model_validate(document)

    async def get_user_documents(self, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> DocumentListResponse:
        docs = await self.doc_repo.get_by_user(user_id, skip, limit)
        total = await self.doc_repo.count_by_user(user_id)
        return DocumentListResponse(documents=[DocumentResponse.model_validate(d) for d in docs], total=total)

    async def delete_document(self, doc_id: uuid.UUID, user_id: uuid.UUID | None = None) -> bool:
        doc = await self.doc_repo.get_by_id(doc_id)
        if not doc or (user_id and doc.uploaded_by != user_id):
            raise NotFoundError("Document not found")

        try:
            ChromaVectorStore().delete_document(doc_id)
        except Exception as e:
            logger.warning("Failed to delete vector chunks for %s: %s", doc_id, e)

        try:
            if os.path.exists(doc.file_path):
                os.remove(doc.file_path)
        except Exception as e:
            logger.error("Failed to delete file from disk: %s", e)

        return await self.doc_repo.delete(doc_id)

    async def process_document(self, document_id: uuid.UUID) -> None:
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc:
            return

        try:
            pages_data = self._load_document(doc.file_path, doc.file_type)
            chunk_texts, metadatas = self._split_documents(pages_data, doc.filename)
            
            chunk_texts = [text.strip() for text in chunk_texts if text.strip()]
            metadatas = metadatas[:len(chunk_texts)]

            embeddings = get_embedding_service().embed_texts(chunk_texts)
            ChromaVectorStore().add_document_chunks(doc, chunk_texts, embeddings, metadatas)

            await self.doc_repo.update_status(document_id, DocumentStatus.ready, len(chunk_texts))
            logger.info("Document %s processed successfully with %s chunks.", document_id, len(chunk_texts))
        except Exception as e:
            logger.error("Error processing document %s: %s", document_id, e)
            await self.doc_repo.update_status(document_id, DocumentStatus.failed)

    def _load_document(self, file_path: str, file_type: str) -> list[dict[str, Any]]:
        """Loads a document and returns a list of pages with page_content and metadata."""
        pages = []
        if file_type == "pdf":
            reader = pypdf.PdfReader(file_path)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                pages.append({
                    "page_content": text,
                    "metadata": {"page": page_num + 1}
                })
        elif file_type == "docx":
            text = docx2txt.process(file_path)
            pages.append({
                "page_content": text,
                "metadata": {"page": 1}
            })
        elif file_type == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            pages.append({
                "page_content": text,
                "metadata": {"page": 1}
            })
        else:
            raise ValueError("Unsupported document type")
        return pages

    def _split_documents(self, pages: list[dict[str, Any]], filename: str) -> tuple[list[str], list[dict[str, Any]]]:
        """A simple, pure-Python recursive-like character text splitter that mimics the chunking logic

        without LangChain dependencies.
        """
        chunk_size = settings.CHUNK_SIZE
        chunk_overlap = settings.CHUNK_OVERLAP
        
        chunk_texts = []
        metadatas = []
        
        for page in pages:
            text = page["page_content"]
            page_meta = page["metadata"]
            
            start = 0
            while start < len(text):
                end = start + chunk_size
                # Try to find a nice place to split (e.g. newline or space)
                if end < len(text):
                    # Look back up to chunk_overlap for a separator
                    last_sep = -1
                    for sep in ["\n\n", "\n", ". ", " "]:
                        pos = text.rfind(sep, start + chunk_size - chunk_overlap, end)
                        if pos != -1:
                            last_sep = pos + len(sep)
                            break
                    if last_sep != -1:
                        end = last_sep
                
                chunk = text[start:end]
                if chunk.strip():
                    chunk_texts.append(chunk)
                    metadatas.append({
                        "page": page_meta.get("page", 1),
                        "source": filename
                    })
                
                start = end - chunk_overlap if end < len(text) else end
                if start >= len(text) or (end >= len(text)):
                    break
                    
        return chunk_texts, metadatas


async def process_document_background(document_id: uuid.UUID) -> None:
    async with async_session_maker() as db:
        await DocumentService(db).process_document(document_id)
