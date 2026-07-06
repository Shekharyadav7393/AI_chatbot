from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings

settings = get_settings()

def setup_cors(app: FastAPI):
    # Browsers block wildcard origins if allow_credentials is True
    allow_creds = "*" not in settings.CORS_ORIGINS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=allow_creds,
        allow_methods=["*"],
        allow_headers=["*"],
    )
