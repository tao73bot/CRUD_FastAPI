from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from dotenv import load_dotenv
import os
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = 'localhost'
    REDIS_PORT : int = 6379

    model_config = SettingsConfigDict(
        env_file = '.env',
        extra = 'ignore'
    )

settings = Settings()


engine = AsyncEngine(
    create_engine(settings.DB_URL, echo=True)
)

async def init_db():
    async with engine.begin() as conn:
        from books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session()->AsyncSession:
    
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with Session() as session:
        try:
            yield session
        finally:
            await session.close()