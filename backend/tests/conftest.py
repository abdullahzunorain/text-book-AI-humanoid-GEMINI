import asyncio
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from unittest.mock import MagicMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# Set env vars BEFORE any app imports that read them at module level
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("GEMINI_API_KEY", "test-key-not-real")
os.environ.setdefault("QDRANT_URL", "")

from src.main import app  # noqa: E402
from src.db.database import Base, get_db  # noqa: E402
from src.services.vector_store import get_qdrant_client  # noqa: E402

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    connection = await test_engine.connect()
    transaction = await connection.begin()

    Session = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    session = Session()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture
def mock_qdrant():
    """Mock QdrantClient for tests that don't need real vector search."""
    mock = MagicMock()
    mock.get_collections.return_value = MagicMock(collections=[])
    mock.search.return_value = []
    return mock


@pytest_asyncio.fixture
async def client(db_session, mock_qdrant) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    def override_get_qdrant():
        return mock_qdrant

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_qdrant_client] = override_get_qdrant

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
