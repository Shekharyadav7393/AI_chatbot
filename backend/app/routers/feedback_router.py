import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.user import User
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.schemas.common import SuccessResponse
from app.controllers.feedback_controller import FeedbackController
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("", response_model=SuccessResponse[FeedbackResponse])
async def submit_feedback(
    request: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await FeedbackController.submit(request, current_user, db)

@router.get("/{message_id}", response_model=SuccessResponse[FeedbackResponse])
async def get_feedback(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user), # Just to protect endpoint
    db: AsyncSession = Depends(get_db)
):
    return await FeedbackController.get(message_id, db)
