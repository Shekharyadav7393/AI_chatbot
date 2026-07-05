import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.feedback import FeedbackRequest
from app.schemas.common import SuccessResponse
from app.services.feedback_service import FeedbackService

class FeedbackController:
    @staticmethod
    async def submit(request: FeedbackRequest, current_user: User, db: AsyncSession):
        service = FeedbackService(db)
        feedback = await service.submit_feedback(request, current_user.id)
        return SuccessResponse(message="Feedback submitted successfully", data=feedback)

    @staticmethod
    async def get(message_id: uuid.UUID, db: AsyncSession):
        service = FeedbackService(db)
        feedback = await service.get_feedback(message_id)
        return SuccessResponse(data=feedback)
