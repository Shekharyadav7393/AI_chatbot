import logging
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession: # type: ignore
    """Dependency for getting async database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Prepare local runtime directories and seed initial admin user if not exists."""
    try:
        Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(parents=True, exist_ok=True)
        logger.info("Runtime directories initialized successfully.")
        
        # Log redacted database URL for debugging connection errors
        db_url = settings.DATABASE_URL
        if "@" in db_url:
            db_url_parts = db_url.split("@")
            redacted_url = "postgresql+asyncpg://<redacted>@" + db_url_parts[-1]
        else:
            redacted_url = db_url
        logger.info(f"Database initialization connecting to: {redacted_url}")
        
        # Seed default admin user
        from sqlalchemy import select
        from app.models.user import User, UserRole
        from app.utils.security import hash_password
        
        async with async_session_maker() as session:
            stmt = select(User).where(User.email == "admin@supportdesk.com")
            result = await session.execute(stmt)
            admin = result.scalars().first()
            if not admin:
                new_admin = User(
                    email="admin@supportdesk.com",
                    username="admin",
                    hashed_password=hash_password("AdminPassword123!"),
                    role=UserRole.admin,
                    is_active=True
                )
                session.add(new_admin)
                await session.commit()
                logger.info("Default admin user (admin@supportdesk.com) seeded successfully.")
            else:
                logger.info("Admin user already exists, skipping seed.")
    except Exception as e:
        logger.error(f"Error initializing application directories or seeding: {e}")
