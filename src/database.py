from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
from src.config import Settings

sync_engine = create_engine(
    url=Settings.database_url_psycopg(),
    echo=True,
    pool_pre_ping=True,
)

async_engine = create_async_engine(
    url=Settings.database_url_asyncpg(),
    echo=True,
    pool_pre_ping=True,
    pool_size=32,
    max_overflow=16,
)

session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
