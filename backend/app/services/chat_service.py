import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat import ChatHistoryResponse, ChatDetailResponse, ChatSummary
from app.repositories.chat_repository import ChatRepository
from app.utils.exceptions import NotFoundError

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_repo = ChatRepository(db)

    async def get_history(self, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> ChatHistoryResponse:
        chats = await self.chat_repo.get_by_user(user_id, skip, limit)
        
        chat_summaries = []
        for chat in chats:
            # We would normally do a count query, but for now we'll just say 0 if not loaded
            # or load count from DB. Assuming a relationship or a separate query
            chat_summaries.append(ChatSummary(
                id=chat.id,
                title=chat.title,
                created_at=chat.created_at,
                updated_at=chat.updated_at,
                message_count=0 # Placeholder, ideally we add a subquery in repo
            ))
            
        return ChatHistoryResponse(chats=chat_summaries, total=len(chats))

    async def get_chat_detail(self, chat_id: uuid.UUID, user_id: uuid.UUID) -> ChatDetailResponse:
        chat = await self.chat_repo.get_with_messages(chat_id)
        if not chat or chat.user_id != user_id:
            raise NotFoundError("Chat not found")
            
        return ChatDetailResponse.model_validate(chat)

    async def delete_chat(self, chat_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        chat = await self.chat_repo.get_by_id(chat_id)
        if not chat or chat.user_id != user_id:
            raise NotFoundError("Chat not found")
        return await self.chat_repo.delete(chat_id)

    async def delete_all_history(self, user_id: uuid.UUID) -> int:
        return await self.chat_repo.delete_all_by_user(user_id)
