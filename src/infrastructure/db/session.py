from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config.db_config import setting

async_engine = create_async_engine(url=setting.DATABASE_URL, echo=False)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session():
    async with async_session_factory() as session:
        yield session
