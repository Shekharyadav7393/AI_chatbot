import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.message_repository import MessageRepository
from app.utils.exceptions import NotFoundError, ConflictError

class FeedbackService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.feedback_repo = FeedbackRepository(db)
        self.msg_repo = MessageRepository(db)

    async def submit_feedback(self, data: FeedbackRequest, user_id: uuid.UUID) -> FeedbackResponse:
        # Check if message exists
        msg = await self.msg_repo.get_by_id(data.message_id)
        if not msg:
            raise NotFoundError("Message not found")
            
        # Check if feedback already exists for this message
        existing = await self.feedback_repo.get_by_message(data.message_id)
        if existing:
            # Update existing
            updated = await self.feedback_repo.update(existing.id, {
                "rating": data.rating,
                "comment": data.comment
            })
            return FeedbackResponse.model_validate(updated)
            
        # Create new
        feedback = await self.feedback_repo.create({
            "message_id": data.message_id,
            "user_id": user_id,
            "rating": data.rating,
            "comment": data.comment
        })
        return FeedbackResponse.model_validate(feedback)

    async def get_feedback(self, message_id: uuid.UUID) -> FeedbackResponse:
        feedback = await self.feedback_repo.get_by_message(message_id)
        if not feedback:
            raise NotFoundError("Feedback not found")
        return FeedbackResponse.model_validate(feedback)
