"""
Database configuration and session management for Neon Postgres.
Uses async SQLAlchemy with asyncpg.
"""
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

# Ensure the URL is for asyncpg
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# asyncpg doesn't understand sslmode/channel_binding query params — strip them and use ssl=True
import ssl as _ssl
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

_connect_args: dict = {}
if DATABASE_URL and "asyncpg" in DATABASE_URL:
    _parsed = urlparse(DATABASE_URL)
    _params = parse_qs(_parsed.query)
    _needs_ssl = _params.pop("sslmode", [None])[0] in ("require", "verify-full", "verify-ca")
    _params.pop("channel_binding", None)  # asyncpg doesn't support this param
    _clean_query = urlencode({k: v[0] for k, v in _params.items()}, doseq=False)
    DATABASE_URL = urlunparse(_parsed._replace(query=_clean_query))
    if _needs_ssl:
        _ssl_ctx = _ssl.create_default_context()
        _ssl_ctx.check_hostname = False
        _ssl_ctx.verify_mode = _ssl.CERT_NONE
        _connect_args = {"ssl": _ssl_ctx}

Base = declarative_base()

# Lazily create engine — allows test imports without DATABASE_URL set
engine = None
AsyncSessionLocal = None

if DATABASE_URL:
    engine = create_async_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        echo=False,
        connect_args=_connect_args,
    )

    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def get_db():
    """
    Dependency for FastAPI routes to get database session.
    Usage: db: AsyncSession = Depends(get_db)
    """
    if not AsyncSessionLocal:
        raise RuntimeError(
            "DATABASE_URL is not configured. "
            "Set it in your .env file or environment variables."
        )
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
