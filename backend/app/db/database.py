from collections.abc import Generator

from sqlalchemy import Engine, create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def ensure_schema_upgrades(bind_engine: Engine) -> None:
    """Idempotently add RBAC & security columns to existing PostgreSQL / SQLite tables."""
    inspector = inspect(bind_engine)
    if "users" not in inspector.get_table_names():
        return

    existing_cols = {col["name"] for col in inspector.get_columns("users")}
    statements: list[str] = []
    if "is_active" not in existing_cols:
        statements.append("ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE")
    if "token_version" not in existing_cols:
        statements.append("ALTER TABLE users ADD COLUMN token_version INTEGER NOT NULL DEFAULT 1")

    if statements:
        with bind_engine.begin() as conn:
            for stmt in statements:
                conn.execute(text(stmt))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
