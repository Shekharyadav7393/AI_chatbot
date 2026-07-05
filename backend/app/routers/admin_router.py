import uuid
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.user import User
from app.schemas.admin import DashboardResponse, AdminUserUpdate
from app.schemas.user import UserListResponse, UserResponse
from app.schemas.document import DocumentListResponse, DocumentResponse
from app.schemas.common import SuccessResponse
from app.controllers.admin_controller import AdminController
from app.middleware.auth_middleware import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard", response_model=SuccessResponse[DashboardResponse])
async def get_dashboard(
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await AdminController.dashboard(db)

@router.get("/users", response_model=SuccessResponse[UserListResponse])
async def list_users(
    skip: int = 0,
    limit: int = 20,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await AdminController.list_users(db, skip, limit)

@router.put("/users/{user_id}", response_model=SuccessResponse[UserResponse])
async def update_user(
    user_id: uuid.UUID,
    request: AdminUserUpdate,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await AdminController.update_user(user_id, request, db)

@router.delete("/users/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: uuid.UUID,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await AdminController.delete_user(user_id, db)

@router.get("/documents", response_model=SuccessResponse[DocumentListResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await AdminController.list_documents(db, skip, limit)

@router.delete("/documents/{doc_id}", response_model=SuccessResponse)
async def delete_document(
    doc_id: uuid.UUID,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await AdminController.delete_document(doc_id, db)

@router.post("/documents/upload", response_model=SuccessResponse[DocumentResponse])
async def upload_knowledge_base(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await AdminController.upload_kb(file, current_admin, db, background_tasks)
