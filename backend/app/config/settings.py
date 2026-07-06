from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "AI Customer Support Chatbot"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatbot_db"
    
    # JWT Auth
    JWT_SECRET_KEY: str = "super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AI provider. Use "auto" to prefer Gemini when GEMINI_API_KEY is set,
    # otherwise fall back to the local Hugging Face model.
    AI_PROVIDER: str = "auto"

    # Gemini API
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_API_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"
    GEMINI_TIMEOUT_SECONDS: float = 60.0
    
    # Local offline language model. Use a local path or a model already cached by Hugging Face.
    LOCAL_LLM_MODEL: str = "google/flan-t5-base"
    LOCAL_LLM_TASK: str = "text2text-generation"
    LOCAL_LLM_MAX_NEW_TOKENS: int = 256
    LOCAL_LLM_TEMPERATURE: float = 0.1
    TRANSFORMERS_OFFLINE: bool = True
    
    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    VECTOR_DIMENSION: int = 384
    
    # ChromaDB
    CHROMA_PERSIST_DIR: str = "vectorstore/chroma"
    CHROMA_COLLECTION_NAME: str = "company_knowledge_base"
    
    # Uploads
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10485760 # 10MB
    
    # CORS & Rate Limiting
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    RATE_LIMIT: str = "100/minute"
    
    # RAG
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5
    RETRIEVAL_SCORE_THRESHOLD: float = 0.35
    
    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def sync_database_url(self) -> str:
        return self.DATABASE_URL.replace("+asyncpg", "")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Convert Render's postgres:// or postgresql:// to postgresql+asyncpg:// for async SQLAlchemy
        if self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
        elif self.DATABASE_URL.startswith("postgresql://") and not self.DATABASE_URL.startswith("postgresql+asyncpg://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
            
        # If in production (e.g. on Render) or DEBUG is False, ensure CORS is open
        import os
        if (not self.DEBUG or os.environ.get("RENDER")) and "http://localhost:5173" in self.CORS_ORIGINS:
            self.CORS_ORIGINS = ["*"]

@lru_cache()
def get_settings() -> Settings:
    """Returns a cached instance of the settings."""
    return Settings()
