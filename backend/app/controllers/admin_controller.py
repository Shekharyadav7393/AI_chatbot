import uuid
from fastapi import UploadFile, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.admin import AdminUserUpdate
from app.schemas.common import SuccessResponse
from app.services.admin_service import AdminService
from app.services.document_service import process_document_background

class AdminController:
    @staticmethod
    async def dashboard(db: AsyncSession):
        service = AdminService(db)
        data = await service.get_dashboard()
        return SuccessResponse(data=data)

    @staticmethod
    async def list_users(db: AsyncSession, skip: int = 0, limit: int = 20):
        service = AdminService(db)
        data = await service.get_all_users(skip, limit)
        return SuccessResponse(data=data)

    @staticmethod
    async def update_user(user_id: uuid.UUID, request: AdminUserUpdate, db: AsyncSession):
        service = AdminService(db)
        user = await service.update_user(user_id, request)
        return SuccessResponse(message="User updated successfully", data=user)

    @staticmethod
    async def delete_user(user_id: uuid.UUID, db: AsyncSession):
        service = AdminService(db)
        await service.delete_user(user_id)
        return SuccessResponse(message="User deleted successfully")

    @staticmethod
    async def list_documents(db: AsyncSession, skip: int = 0, limit: int = 20):
        service = AdminService(db)
        data = await service.get_all_documents(skip, limit)
        return SuccessResponse(data=data)

    @staticmethod
    async def delete_document(doc_id: uuid.UUID, db: AsyncSession):
        service = AdminService(db)
        await service.delete_document(doc_id)
        return SuccessResponse(message="Document deleted successfully")

    @staticmethod
    async def upload_kb(file: UploadFile, current_user: User, db: AsyncSession, background_tasks: BackgroundTasks):
        admin_service = AdminService(db)
        document = await admin_service.upload_knowledge_base(file, current_user.id)
        background_tasks.add_task(process_document_background, document.id)
        
        return SuccessResponse(message="Knowledge base document uploaded and processing", data=document)
