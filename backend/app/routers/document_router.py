import uuid
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.user import User
from app.schemas.document import DocumentResponse, DocumentListResponse
from app.schemas.common import SuccessResponse
from app.controllers.document_controller import DocumentController
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/documents", tags=["Documents"])
alias_router = APIRouter(tags=["Documents"])

@router.post("/upload", response_model=SuccessResponse[DocumentResponse])
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await DocumentController.upload(file, current_user, db, background_tasks)

@router.get("", response_model=SuccessResponse[DocumentListResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await DocumentController.list_documents(current_user, db, skip, limit)

@router.delete("/{doc_id}", response_model=SuccessResponse)
async def delete_document(
    doc_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await DocumentController.delete(doc_id, current_user, db)


@alias_router.post("/upload", response_model=SuccessResponse[DocumentResponse])
async def upload_document_alias(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await DocumentController.upload(file, current_user, db, background_tasks)
