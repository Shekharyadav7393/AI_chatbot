from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings

settings = get_settings()

def setup_cors(app: FastAPI):
    # Filter out empty values
    origins = [o for o in settings.CORS_ORIGINS if o]
    allow_creds = "*" not in origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_creds,
        allow_methods=["*"],
        allow_headers=["*"],
    )
