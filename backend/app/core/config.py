import os

KNOWN_WEAK_SECRETS: frozenset[str] = frozenset(
    {
        "",
        "secret",
        "changeme",
        "search-want-super-secret-dev-key-change-in-production-2026",
        "change-this-to-a-strong-production-secret",
    }
)


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _parse_cors_origins(raw: str | None, is_production: bool) -> list[str]:
    if raw and raw.strip():
        origins = [item.strip() for item in raw.split(",") if item.strip()]
        if origins:
            return origins
    # In production without explicit wildcard, default to empty cross-origin list (same-origin Nitro/Nginx still works)
    return [] if is_production else ["*"]


class Settings:
    APP_NAME: str = "Search-Want API"
    APP_VERSION: str = "1.0.0"

    APP_ENV: str = os.getenv("SEARCH_WANT_ENV", "development").strip().lower()
    IS_PRODUCTION: bool = APP_ENV == "production"

    SECRET_KEY: str = os.getenv(
        "SEARCH_WANT_SECRET_KEY",
        "search-want-super-secret-dev-key-change-in-production-2026",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv(
            "SEARCH_WANT_TOKEN_EXPIRE_MINUTES",
            str(60 * 12 if IS_PRODUCTION else 60 * 24 * 7),
        )
    )

    # Security & Environment Feature Gates
    DEMO_MODE: bool = _env_bool("SEARCH_WANT_DEMO_MODE", default=not IS_PRODUCTION)
    ENABLE_DOCS: bool = _env_bool("SEARCH_WANT_ENABLE_DOCS", default=not IS_PRODUCTION)
    CORS_ORIGINS: list[str] = _parse_cors_origins(
        os.getenv("SEARCH_WANT_CORS_ORIGINS"), IS_PRODUCTION
    )

    # Optional Production Bootstrap Super Admin (Creates/Upgrades real owner account without demo passwords)
    BOOTSTRAP_SUPER_ADMIN_EMAIL: str = os.getenv("SEARCH_WANT_SUPER_ADMIN_EMAIL", "").strip().lower()
    BOOTSTRAP_SUPER_ADMIN_PASSWORD: str = os.getenv("SEARCH_WANT_SUPER_ADMIN_PASSWORD", "").strip()
    BOOTSTRAP_SUPER_ADMIN_NAME: str = os.getenv(
        "SEARCH_WANT_SUPER_ADMIN_NAME", "ຜູ້ບໍລິຫານສູງສຸດ"
    ).strip()

    DATABASE_URL: str = os.getenv(
        "SEARCH_WANT_DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/search_want",
    )
    ADSENSE_CLIENT_ID: str = os.getenv(
        "SEARCH_WANT_ADSENSE_CLIENT_ID", "ca-pub-4990570878383229"
    )
    ADSENSE_SLOT_INFEED: str = os.getenv("SEARCH_WANT_ADSENSE_SLOT_INFEED", "6642734194")
    ADSENSE_SLOT_BANNER: str = os.getenv("SEARCH_WANT_ADSENSE_SLOT_BANNER", "8750022785")

    def has_strong_secret_key(self) -> bool:
        key = (self.SECRET_KEY or "").strip()
        return len(key) >= 32 and key not in KNOWN_WEAK_SECRETS

    def is_cors_restricted(self) -> bool:
        return "*" not in self.CORS_ORIGINS

    def validate_production_settings(self) -> None:
        if not self.IS_PRODUCTION:
            return
        if not self.has_strong_secret_key():
            raise RuntimeError(
                "PRODUCTION SECURITY ERROR: SEARCH_WANT_SECRET_KEY ຕ້ອງມີຄວາມຍາວຢ່າງໜ້ອຍ 32 ຕົວອັກສອນ "
                "ແລະ ຫ້າມໃຊ້ຄ່າເລີ່ມຕົ້ນຂອງໂໝດພັດທະນາ ເມື່ອຕັ້ງ SEARCH_WANT_ENV=production."
            )
        if self.BOOTSTRAP_SUPER_ADMIN_EMAIL and len(self.BOOTSTRAP_SUPER_ADMIN_PASSWORD) < 8:
            raise RuntimeError(
                "PRODUCTION SECURITY ERROR: SEARCH_WANT_SUPER_ADMIN_PASSWORD ຕ້ອງມີຢ່າງໜ້ອຍ 8 ຕົວອັກສອນ."
            )


settings = Settings()
