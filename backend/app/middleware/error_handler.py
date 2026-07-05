from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.exceptions import AppException
from app.schemas.common import ErrorResponse, ErrorDetail
from app.utils.logger import get_logger

logger = get_logger(__name__)

def setup_exception_handlers(app: FastAPI):
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(f"AppException: {exc.error_code} - {exc.message}")
        error_response = ErrorResponse(
            success=False,
            error=ErrorDetail(code=exc.error_code, message=exc.message)
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation Error: {exc.errors()}")
        error_response = ErrorResponse(
            success=False,
            error=ErrorDetail(code="VALIDATION_ERROR", message="Invalid request parameters")
        )
        return JSONResponse(
            status_code=422,
            content=error_response.model_dump()
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        error_response = ErrorResponse(
            success=False,
            error=ErrorDetail(code="INTERNAL_SERVER_ERROR", message="An unexpected error occurred")
        )
        return JSONResponse(
            status_code=500,
            content=error_response.model_dump()
        )
