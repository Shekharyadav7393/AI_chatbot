from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.settings import get_settings
from app.database.session import init_db
from app.utils.logger import setup_logging, get_logger
from app.middleware.cors import setup_cors
from app.middleware.error_handler import setup_exception_handlers
from app.middleware.rate_limiter import limiter
from slowapi.middleware import SlowAPIMiddleware

# Import routers
from app.routers.auth_router import router as auth_router
from app.routers.auth_router import alias_router as auth_alias_router
from app.routers.user_router import router as user_router
from app.routers.user_router import alias_router as user_alias_router
from app.routers.document_router import router as document_router
from app.routers.document_router import alias_router as document_alias_router
from app.routers.chat_router import router as chat_router
from app.routers.chat_router import alias_router as chat_alias_router
from app.routers.feedback_router import router as feedback_router
from app.routers.admin_router import router as admin_router

settings = get_settings()
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up application...")
    
    # Initialize runtime directories; schema is managed with Alembic.
    await init_db()
    
    yield
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise AI Customer Support Chatbot API",
    version="1.0.0",
    lifespan=lifespan
)

# Setup Middlewares
setup_cors(app)
setup_exception_handlers(app)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Include Routers
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_alias_router, prefix=settings.API_V1_PREFIX)
app.include_router(user_router, prefix=settings.API_V1_PREFIX)
app.include_router(user_alias_router, prefix=settings.API_V1_PREFIX)
app.include_router(document_router, prefix=settings.API_V1_PREFIX)
app.include_router(document_alias_router, prefix=settings.API_V1_PREFIX)
app.include_router(chat_router, prefix=settings.API_V1_PREFIX)
app.include_router(chat_alias_router, prefix=settings.API_V1_PREFIX)
app.include_router(feedback_router, prefix=settings.API_V1_PREFIX)
app.include_router(admin_router, prefix=settings.API_V1_PREFIX)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.APP_NAME,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
