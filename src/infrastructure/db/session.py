from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config.db_config import setting


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


db_helper = DataBaseHelper(url=setting.DATABASE_URL)


async def get_async_session():
    async for session in db_helper.get_session():
        yield session
