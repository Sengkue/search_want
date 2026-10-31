from app.db.models import Shop
from app.schemas.schemas import ShopOut


def shop_to_out(
    shop: Shop,
    distance_km: float | None = None,
    match_score: int = 0,
    matched_reasons: list[str] | None = None,
    include_owner_email: bool = False,
) -> ShopOut:
    return ShopOut(
        id=shop.id,
        owner_id=shop.owner_id,
        owner_name=shop.owner.full_name if shop.owner else "Shop Owner",
        owner_email=(shop.owner.email if (include_owner_email and shop.owner) else None),
        category_id=shop.category_id,
        category_name=shop.category.name if shop.category else "General",
        category_slug=shop.category.slug if shop.category else "general",
        category_icon=shop.category.icon if shop.category else "mdi-store-marker",
        category_color=shop.category.color if shop.category else "#1976D2",
        name=shop.name,
        description=shop.description,
        problem_tags=shop.problem_tags,
        phone=shop.phone,
        address=shop.address,
        latitude=shop.latitude,
        longitude=shop.longitude,
        opening_hours=shop.opening_hours,
        is_emergency_24h=shop.is_emergency_24h,
        status=shop.status,
        rejection_reason=shop.rejection_reason,
        distance_km=distance_km,
        match_score=match_score,
        matched_reasons=matched_reasons or [],
        created_at=shop.created_at,
        updated_at=shop.updated_at,
    )

