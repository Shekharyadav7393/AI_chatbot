import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.chat import ChatRequest
from app.schemas.common import SuccessResponse
from app.services.chat_service import ChatService
from app.services.rag_service import RAGService

class ChatController:
    @staticmethod
    async def chat(request: ChatRequest, current_user: User, db: AsyncSession):
        service = RAGService(db)
        response = await service.chat(request.message, request.chat_id, current_user.id)
        return SuccessResponse(data=response)

    @staticmethod
    async def get_history(current_user: User, db: AsyncSession, skip: int = 0, limit: int = 20):
        service = ChatService(db)
        history = await service.get_history(current_user.id, skip, limit)
        return SuccessResponse(data=history)

    @staticmethod
    async def get_chat(chat_id: uuid.UUID, current_user: User, db: AsyncSession):
        service = ChatService(db)
        chat = await service.get_chat_detail(chat_id, current_user.id)
        return SuccessResponse(data=chat)

    @staticmethod
    async def delete_chat(chat_id: uuid.UUID, current_user: User, db: AsyncSession):
        service = ChatService(db)
        await service.delete_chat(chat_id, current_user.id)
        return SuccessResponse(message="Chat deleted successfully")

    @staticmethod
    async def delete_all_history(current_user: User, db: AsyncSession):
        service = ChatService(db)
        count = await service.delete_all_history(current_user.id)
        return SuccessResponse(message=f"Deleted {count} chats successfully")
