from datetime import datetime, timezone
from xml.sax.saxutils import escape

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.db.models import Category, Shop

router = APIRouter(tags=["SEO & Search Crawlers"])


def _resolve_site_origin(request: Request) -> str:
    if settings.SITE_URL:
        return settings.SITE_URL
    proto = (
        request.headers.get("x-forwarded-proto")
        or request.url.scheme
        or "https"
    ).split(",")[0].strip()
    host = (
        request.headers.get("x-forwarded-host")
        or request.headers.get("host")
        or request.url.netloc
        or "localhost:3000"
    ).split(",")[0].strip()
    return f"{proto}://{host}".rstrip("/")


@router.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml(request: Request, db: Session = Depends(get_db)) -> Response:
    """Dynamic XML Sitemap listing core pages, service categories, and all APPROVED local shops."""
    origin = _resolve_site_origin(request)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    categories = db.query(Category).order_by(Category.id.asc()).all()
    approved_shops = (
        db.query(Shop)
        .filter(Shop.status == "APPROVED")
        .order_by(Shop.updated_at.desc(), Shop.id.desc())
        .all()
    )

    urls: list[tuple[str, str, str, str]] = [
        (f"{origin}/", today, "daily", "1.0"),
        (f"{origin}/shops/add", today, "monthly", "0.75"),
        (f"{origin}/privacy", today, "yearly", "0.40"),
    ]

    for cat in categories:
        urls.append((f"{origin}/?category={cat.id}", today, "daily", "0.85"))

    for shop in approved_shops:
        lastmod = (
            shop.updated_at.strftime("%Y-%m-%d")
            if getattr(shop, "updated_at", None)
            else today
        )
        urls.append((f"{origin}/shops/{shop.id}", lastmod, "weekly", "0.90"))

    xml_entries = "\n".join(
        f"  <url>\n"
        f"    <loc>{escape(loc)}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n"
        f"    <priority>{prio}</priority>\n"
        f"  </url>"
        for loc, lastmod, freq, prio in urls
    )

    xml_body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{xml_entries}\n"
        "</urlset>\n"
    )

    return Response(
        content=xml_body,
        media_type="application/xml; charset=utf-8",
        headers={"Cache-Control": "public, max-age=1800, s-maxage=1800"},
    )
