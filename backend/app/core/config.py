import os


class Settings:
    APP_NAME: str = "Search-Want API"
    APP_VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv(
        "SEARCH_WANT_SECRET_KEY",
        "search-want-super-secret-dev-key-change-in-production-2026",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    DATABASE_URL: str = os.getenv(
        "SEARCH_WANT_DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/search_want",
    )
    ADSENSE_CLIENT_ID: str = os.getenv(
        "SEARCH_WANT_ADSENSE_CLIENT_ID", "ca-pub-4990570878383229"
    )
    ADSENSE_SLOT_INFEED: str = os.getenv("SEARCH_WANT_ADSENSE_SLOT_INFEED", "")
    ADSENSE_SLOT_BANNER: str = os.getenv("SEARCH_WANT_ADSENSE_SLOT_BANNER", "8750022785")


settings = Settings()

