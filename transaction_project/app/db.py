import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.config import DATABASE_URL, USE_POSTGRES
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print(DATABASE_URL)
if not USE_POSTGRES:
    engine = create_async_engine(
        "sqlite+aiosqlite:///./sql_app.db", connect_args={"check_same_thread": False}
    )
else:
    engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore

Base = declarative_base()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = SessionLocal()  # type: ignore
    try:
        yield session
    finally:
        await session.close()
