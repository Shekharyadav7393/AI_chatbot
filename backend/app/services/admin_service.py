import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from app.schemas.admin import DashboardResponse, ActivityItem, AdminUserUpdate
from app.schemas.user import UserListResponse, UserResponse
from app.schemas.document import DocumentListResponse, DocumentResponse
from app.repositories.user_repository import UserRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.services.document_service import DocumentService
from app.utils.exceptions import NotFoundError

class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.doc_repo = DocumentRepository(db)
        self.chat_repo = ChatRepository(db)
        self.msg_repo = MessageRepository(db)
        self.feedback_repo = FeedbackRepository(db)
        self.doc_service = DocumentService(db)

    async def get_dashboard(self) -> DashboardResponse:
        total_users = await self.user_repo.count()
        total_documents = await self.doc_repo.count()
        total_chats = await self.chat_repo.count()
        total_messages = await self.msg_repo.count()
        total_feedback = await self.feedback_repo.count()
        avg_rating = await self.feedback_repo.get_average_rating()
        
        # Get recent activity (e.g. recent feedback)
        recent_feedbacks = await self.feedback_repo.get_recent(limit=5)
        recent_activity = [
            ActivityItem(
                type="feedback",
                description=f"Received {f.rating}-star feedback",
                timestamp=f.created_at
            ) for f in recent_feedbacks
        ]

        return DashboardResponse(
            total_users=total_users,
            total_documents=total_documents,
            total_chats=total_chats,
            total_messages=total_messages,
            total_feedback=total_feedback,
            avg_rating=round(avg_rating, 2),
            recent_activity=recent_activity
        )

    async def get_all_users(self, skip: int = 0, limit: int = 20) -> UserListResponse:
        users = await self.user_repo.get_all(skip, limit)
        total = await self.user_repo.count()
        return UserListResponse(
            users=[UserResponse.model_validate(u) for u in users],
            total=total
        )

    async def update_user(self, user_id: uuid.UUID, data: AdminUserUpdate) -> UserResponse:
        update_data = data.model_dump(exclude_unset=True)
        user = await self.user_repo.update(user_id, update_data)
        if not user:
            raise NotFoundError("User not found")
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: uuid.UUID) -> bool:
        success = await self.user_repo.delete(user_id)
        if not success:
            raise NotFoundError("User not found")
        return success

    async def get_all_documents(self, skip: int = 0, limit: int = 20) -> DocumentListResponse:
        docs = await self.doc_repo.get_all(skip, limit)
        total = await self.doc_repo.count()
        return DocumentListResponse(
            documents=[DocumentResponse.model_validate(d) for d in docs],
            total=total
        )

    async def delete_document(self, doc_id: uuid.UUID) -> bool:
        # Use doc service so it deletes the file from disk too
        return await self.doc_service.delete_document(doc_id)

    async def upload_knowledge_base(self, file: UploadFile, admin_id: uuid.UUID) -> DocumentResponse:
        return await self.doc_service.upload_document(file, admin_id)
