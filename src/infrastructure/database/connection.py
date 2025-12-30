from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.infrastructure.config.settings import settings

class PostgreDBConnection:
    
    _engine = None
    _session_factory = None

    @classmethod
    def initialize(cls, database_url: str = None):
        if database_url is None:
            database_url = settings.DATABASE_URL

        cls._engine = create_async_engine(
            database_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            echo=settings.DEBUG,
        )

        cls._session_factory = async_sessionmaker(
            bind=cls._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls.initialize()
        return cls._engine

    @classmethod
    def get_session_factory(cls):
        if cls._session_factory is None:
            cls.initialize()
        return cls._session_factory

    @classmethod
    async def close(cls):
        if cls._engine is not None:
            await cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_factory = PostgreDBConnection.get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise