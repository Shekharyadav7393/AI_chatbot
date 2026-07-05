import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse, ChatDetailResponse
from app.schemas.common import SuccessResponse
from app.controllers.chat_controller import ChatController
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])
alias_router = APIRouter(tags=["Chat"])

@router.post("", response_model=SuccessResponse[ChatResponse])
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ChatController.chat(request, current_user, db)

@router.get("/history", response_model=SuccessResponse[ChatHistoryResponse])
async def get_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ChatController.get_history(current_user, db, skip, limit)

@router.get("/{chat_id}", response_model=SuccessResponse[ChatDetailResponse])
async def get_chat(
    chat_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ChatController.get_chat(chat_id, current_user, db)

@router.delete("/history/all", response_model=SuccessResponse)
async def delete_all_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ChatController.delete_all_history(current_user, db)

@router.delete("/{chat_id}", response_model=SuccessResponse)
async def delete_chat(
    chat_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ChatController.delete_chat(chat_id, current_user, db)


@alias_router.get("/history", response_model=SuccessResponse[ChatHistoryResponse])
async def get_history_alias(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ChatController.get_history(current_user, db, skip, limit)


@alias_router.delete("/delete-history", response_model=SuccessResponse)
async def delete_all_history_alias(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ChatController.delete_all_history(current_user, db)
