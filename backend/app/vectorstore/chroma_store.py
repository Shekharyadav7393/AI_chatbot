import json
import uuid
from pathlib import Path
from typing import Any

try:
    import chromadb
except ModuleNotFoundError:
    chromadb = None

from app.config.settings import get_settings
from app.models.document import Document
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


class ChromaVectorStore:
    """Persistent vector store adapter for company knowledge-base chunks.

    ChromaDB is used when installed. On Windows machines without native build
    tools, the app falls back to a small JSON-backed cosine store so local
    development can still run.
    """

    _collection: Any | None = None
    _warned_fallback = False

    def __init__(self) -> None:
        Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        self.fallback_path = Path(settings.CHROMA_PERSIST_DIR) / "fallback_vectors.json"
        if chromadb is None:
            self.collection = None
            if not ChromaVectorStore._warned_fallback:
                logger.warning(
                    "chromadb is not installed; using JSON vector store fallback at %s",
                    self.fallback_path,
                )
                ChromaVectorStore._warned_fallback = True
            return

        if ChromaVectorStore._collection is None:
            client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
            ChromaVectorStore._collection = client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
        self.collection = ChromaVectorStore._collection

    def add_document_chunks(
        self,
        document: Document,
        chunk_texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        if not chunk_texts:
            return

        safe_metadatas: list[dict[str, Any]] = []
        for index, metadata in enumerate(metadatas):
            safe_metadatas.append(
                {
                    "document_id": str(document.id),
                    "document_name": document.filename,
                    "file_type": document.file_type,
                    "chunk_index": index,
                    "source": str(metadata.get("source", document.file_path)),
                    "page": metadata.get("page", ""),
                    "uploaded_by": str(document.uploaded_by),
                }
            )

        ids = [f"{document.id}:{index}" for index in range(len(chunk_texts))]
        if self.collection is None:
            records = [record for record in self._load_records() if record.get("id") not in ids]
            records.extend(
                {
                    "id": record_id,
                    "document": chunk_text,
                    "embedding": embedding,
                    "metadata": metadata,
                }
                for record_id, chunk_text, embedding, metadata in zip(
                    ids,
                    chunk_texts,
                    embeddings,
                    safe_metadatas,
                    strict=False,
                )
            )
            self._save_records(records)
            logger.info("Stored %s chunks in JSON vector store for document %s", len(chunk_texts), document.id)
            return

        self.collection.upsert(
            ids=ids,
            documents=chunk_texts,
            embeddings=embeddings,
            metadatas=safe_metadatas,
        )
        logger.info("Stored %s chunks in ChromaDB for document %s", len(chunk_texts), document.id)

    def delete_document(self, document_id: uuid.UUID) -> None:
        if self.collection is None:
            document_id_str = str(document_id)
            records = [
                record
                for record in self._load_records()
                if record.get("metadata", {}).get("document_id") != document_id_str
            ]
            self._save_records(records)
            logger.info("Deleted JSON vector store chunks for document %s", document_id)
            return

        self.collection.delete(where={"document_id": str(document_id)})
        logger.info("Deleted ChromaDB chunks for document %s", document_id)

    def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int,
        score_threshold: float,
    ) -> list[dict[str, Any]]:
        if self.collection is None:
            matches = []
            for record in self._load_records():
                score = self._cosine_similarity(query_embedding, record.get("embedding", []))
                if score < score_threshold:
                    continue

                metadata = record.get("metadata", {})
                matches.append(
                    {
                        "chunk_text": record.get("document", ""),
                        "score": score,
                        "document_id": metadata.get("document_id"),
                        "document_name": metadata.get("document_name", "Unknown"),
                        "chunk_index": metadata.get("chunk_index", 0),
                        "metadata": metadata,
                    }
                )
            return sorted(matches, key=lambda item: item["score"], reverse=True)[:top_k]

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        matches: list[dict[str, Any]] = []
        for chunk_text, metadata, distance in zip(documents, metadatas, distances, strict=False):
            score = max(0.0, 1.0 - float(distance))
            if score < score_threshold:
                continue
            matches.append(
                {
                    "chunk_text": chunk_text,
                    "score": score,
                    "document_id": metadata.get("document_id"),
                    "document_name": metadata.get("document_name", "Unknown"),
                    "chunk_index": metadata.get("chunk_index", 0),
                    "metadata": metadata,
                }
            )
        return matches

    def _load_records(self) -> list[dict[str, Any]]:
        if not self.fallback_path.exists():
            return []

        try:
            payload = json.loads(self.fallback_path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                return payload
        except json.JSONDecodeError as exc:
            logger.warning("Could not read JSON vector store %s: %s", self.fallback_path, exc)
        return []

    def _save_records(self, records: list[dict[str, Any]]) -> None:
        temp_path = self.fallback_path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(records), encoding="utf-8")
        temp_path.replace(self.fallback_path)

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        if not left or not right or len(left) != len(right):
            return 0.0

        dot = sum(a * b for a, b in zip(left, right, strict=False))
        left_norm = sum(value * value for value in left) ** 0.5
        right_norm = sum(value * value for value in right) ** 0.5
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return dot / (left_norm * right_norm)
