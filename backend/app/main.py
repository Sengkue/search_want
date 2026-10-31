from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.database import Base, SessionLocal, engine, ensure_schema_upgrades
from app.db.seed import seed_initial_data
from app.routers import admin, adsense, auth, categories, notifications, shops


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    settings.validate_production_settings()
    Base.metadata.create_all(bind=engine)
    ensure_schema_upgrades(engine)
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "ແພລດຟອມຄົ້ນຫາຮ້ານໃກ້ຄຽງຈາກບັນຫາຂອງທ່ານ ແລະ ໄດເຣັກທໍຣີຮ້ານທີ່ເຈົ້າຂອງຮ້ານເພີ່ມເອງ "
        "ພ້ອມຂະບວນການອະນຸມັດ ແລະ ການແບ່ງສິດລະດັບສູງ (RBAC)."
    ),
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)


@app.middleware("http")
async def security_headers_and_docs_guard(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    # Block OpenAPI schema & Swagger/ReDoc enumeration when ENABLE_DOCS is False (Production default)
    if not settings.ENABLE_DOCS and request.url.path in ("/docs", "/redoc", "/openapi.json"):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "geolocation=(self)")
    return response


_STATIC_DIR = Path(__file__).resolve().parent / "static"
if _STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")

_LAO_FONT_STYLE = """
<style>
@font-face {
  font-family: 'Noto Sans Lao Looped';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('/static/fonts/NotoSansLaoLooped-lao.woff2') format('woff2');
  unicode-range: U+0E81-0EDF, U+200C-200D, U+25CC;
}
@font-face {
  font-family: 'Noto Sans Lao Looped';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('/static/fonts/NotoSansLaoLooped-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+2000-206F;
}
body, .swagger-ui, .swagger-ui *:not(code):not(pre) {
  font-family: 'Noto Sans Lao Looped', 'Noto Sans Lao', 'Phetsarath OT', sans-serif !important;
}
</style>
"""


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html() -> HTMLResponse:
    if not settings.ENABLE_DOCS:
        raise HTTPException(status_code=404, detail="Not Found")
    base = get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=f"{settings.APP_NAME} — API Docs",
    )
    body = base.body.decode("utf-8").replace("</head>", f"{_LAO_FONT_STYLE}</head>")
    return HTMLResponse(content=body)


@app.get("/redoc", include_in_schema=False)
def custom_redoc_html() -> HTMLResponse:
    if not settings.ENABLE_DOCS:
        raise HTTPException(status_code=404, detail="Not Found")
    base = get_redoc_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=f"{settings.APP_NAME} — ReDoc",
    )
    body = base.body.decode("utf-8").replace("</head>", f"{_LAO_FONT_STYLE}</head>")
    return HTMLResponse(content=body)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(shops.router)
app.include_router(admin.router)
app.include_router(notifications.router)
app.include_router(adsense.router)


@app.get("/api/health", tags=["Health"])
def health_check() -> dict[str, object]:
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "env": settings.APP_ENV,
    }


def _resolve_apk_path() -> Path | None:
    project_root = Path(__file__).resolve().parents[2]
    candidates = [
        project_root / "dist" / "SearchWant-release.apk",
        project_root / "dist" / "SearchWant.apk",
        project_root / "dist" / "SearchWant-debug.apk",
        project_root
        / "frontend"
        / "android"
        / "app"
        / "build"
        / "outputs"
        / "apk"
        / "debug"
        / "app-debug.apk",
    ]
    for path in candidates:
        if path.is_file():
            return path
    return None


@app.get("/api/app/apk-info", tags=["Mobile APK"])
def get_apk_info() -> dict[str, object]:
    apk_path = _resolve_apk_path()
    if not apk_path:
        return {
            "available": False,
            "filename": "Search-Want.apk",
            "size_bytes": 0,
            "size_mb": 0.0,
            "version": settings.APP_VERSION,
        }
    size_bytes = apk_path.stat().st_size
    return {
        "available": True,
        "filename": "Search-Want.apk",
        "size_bytes": size_bytes,
        "size_mb": round(size_bytes / (1024 * 1024), 2),
        "version": settings.APP_VERSION,
    }


@app.get("/api/app/apk", tags=["Mobile APK"])
def download_android_apk() -> FileResponse:
    apk_path = _resolve_apk_path()
    if not apk_path:
        raise HTTPException(
            status_code=404,
            detail="ຍັງບໍ່ພົບໄຟລ໌ APK ໃນເຊີບເວີ. ກະລຸນາສັ່ງ npm run android:apk ກ່ອນ.",
        )
    return FileResponse(
        path=apk_path,
        media_type="application/vnd.android.package-archive",
        filename="Search-Want.apk",
    )
