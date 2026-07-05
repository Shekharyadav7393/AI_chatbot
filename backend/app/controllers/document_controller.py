import uuid
from fastapi import UploadFile, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.services.document_service import DocumentService, process_document_background
from app.utils.logger import get_logger

logger = get_logger(__name__)

class DocumentController:
    @staticmethod
    async def upload(file: UploadFile, current_user: User, db: AsyncSession, background_tasks: BackgroundTasks):
        service = DocumentService(db)
        document = await service.upload_document(file, current_user.id)
        
        # Trigger background processing
        background_tasks.add_task(process_document_background, document.id)
        
        return SuccessResponse(message="Document uploaded and is being processed", data=document)

    @staticmethod
    async def list_documents(current_user: User, db: AsyncSession, skip: int = 0, limit: int = 20):
        service = DocumentService(db)
        docs = await service.get_user_documents(current_user.id, skip, limit)
        return SuccessResponse(data=docs)

    @staticmethod
    async def delete(doc_id: uuid.UUID, current_user: User, db: AsyncSession):
        service = DocumentService(db)
        await service.delete_document(doc_id, current_user.id)
        return SuccessResponse(message="Document deleted successfully")
