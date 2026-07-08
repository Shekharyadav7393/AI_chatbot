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
            
        # Strip sslmode from DATABASE_URL if present, as asyncpg doesn't support it
        if "sslmode=" in self.DATABASE_URL:
            from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
            parsed = urlparse(self.DATABASE_URL)
            query = parse_qs(parsed.query)
            query.pop("sslmode", None)
            new_query = urlencode(query, doseq=True)
            self.DATABASE_URL = urlunparse(parsed._replace(query=new_query))
            
        # Map Render's SECRET_KEY to JWT_SECRET_KEY if JWT_SECRET_KEY is default or not set
        import os
        secret_key_env = os.environ.get("SECRET_KEY")
        if secret_key_env and (self.JWT_SECRET_KEY == "super-secret-key" or not os.environ.get("JWT_SECRET_KEY")):
            self.JWT_SECRET_KEY = secret_key_env

        # Parse CORS_ORIGINS from environment variable if it's set as a string
        import json
        cors_env = os.environ.get("CORS_ORIGINS")
        if cors_env:
            try:
                # Try parsing as JSON list
                parsed = json.loads(cors_env)
                if isinstance(parsed, list):
                    self.CORS_ORIGINS = parsed
                elif isinstance(parsed, str):
                    self.CORS_ORIGINS = [parsed]
            except Exception:
                # Fallback to comma-separated list
                self.CORS_ORIGINS = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
        
        # Also allow FRONTEND_URL if provided
        frontend_url = os.environ.get("FRONTEND_URL")
        if frontend_url and frontend_url not in self.CORS_ORIGINS:
            self.CORS_ORIGINS.append(frontend_url)
            
        # If in production (e.g. on Render) or DEBUG is False, and no explicit CORS configuration is provided
        if (not self.DEBUG or os.environ.get("RENDER")) and not os.environ.get("CORS_ORIGINS") and not os.environ.get("FRONTEND_URL"):
            if "http://localhost:5173" in self.CORS_ORIGINS:
                self.CORS_ORIGINS = ["*"]


@lru_cache()
def get_settings() -> Settings:
    """Returns a cached instance of the settings."""
    return Settings()
