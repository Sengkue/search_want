from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Category, ProblemKeyword, Shop
from app.schemas.schemas import CategoryOut, ProblemKeywordOut

router = APIRouter(prefix="/api/categories", tags=["Categories & Symptoms"])


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryOut]:
    counts = dict(
        db.query(Shop.category_id, func.count(Shop.id))
        .filter(Shop.status == "APPROVED")
        .group_by(Shop.category_id)
        .all()
    )
    categories = db.query(Category).order_by(Category.id.asc()).all()
    return [
        CategoryOut(
            id=c.id,
            name=c.name,
            slug=c.slug,
            icon=c.icon,
            color=c.color,
            description=c.description,
            shop_count=counts.get(c.id, 0),
        )
        for c in categories
    ]


@router.get("/symptoms", response_model=list[ProblemKeywordOut])
def list_common_symptoms(db: Session = Depends(get_db)) -> list[ProblemKeywordOut]:
    keywords = db.query(ProblemKeyword).order_by(ProblemKeyword.id.asc()).all()
    seen_labels: set[str] = set()
    unique: list[ProblemKeywordOut] = []
    for kw in keywords:
        if kw.symptom_label not in seen_labels:
            seen_labels.add(kw.symptom_label)
            unique.append(ProblemKeywordOut.model_validate(kw))
    return unique

