import pytest
from httpx import AsyncClient, ASGITransport

from src.infrastructure.db.models.wallet import Base
from src.infrastructure.db.session import DataBaseHelper, get_async_session
from src.main import app

test_db_url = "sqlite+aiosqlite:///:memory:"

test_db_helper = DataBaseHelper(url=test_db_url)


async def override_get_async_session():
    async for session in test_db_helper.get_session():
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True)
async def prepare_database():
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
