import re
from sqlalchemy.orm import Session

from app.db.models import Category, ProblemKeyword, Shop
from app.schemas.schemas import CategoryOut, DiagnosisResult

STOPWORDS = {
    "a", "an", "and", "are", "at", "be", "but", "by", "can", "do", "dont", "don't",
    "fix", "for", "from", "get", "go", "got", "has", "have", "help", "here", "how",
    "i", "idk", "in", "is", "it", "its", "just", "know", "like", "me", "my", "near",
    "need", "no", "not", "now", "of", "on", "or", "please", "problem", "shop", "so",
    "some", "something", "that", "the", "there", "this", "to", "very", "want", "what",
    "when", "where", "which", "with", "yeah", "yes",
}

URGENT_WORDS = {"urgent", "emergency", "sos", "stuck", "highway", "roadside", "night", "24h", "tow"}
# Lao has no spaces between words, so urgent Lao phrases are matched as substrings.
URGENT_PHRASES_LO = ("ດ່ວນ", "ສຸກເສີນ", "ຊ່ວຍດ້ວຍ", "ຕິດກາງທາງ", "ເສຍກາງທາງ", "ກາງຄືນ")


def normalize_text(text: str) -> str:
    cleaned = text.lower().replace("’", "'")
    # Keep ASCII letters/digits and the whole Lao Unicode block (U+0E80–U+0EFF, includes
    # combining vowel/tone marks); everything else becomes a space.
    cleaned = re.sub(r"[^a-z0-9'\s\-\u0e80-\u0eff]", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def extract_tokens(text: str) -> list[str]:
    norm = normalize_text(text)
    if not norm:
        return []
    raw_tokens = norm.replace("'", "").split()
    return [t for t in raw_tokens if len(t) >= 2 and t not in STOPWORDS]


def token_matches_keyword(tokens: list[str], norm_query: str, keyword: str) -> bool:
    kw_norm = normalize_text(keyword)
    if not kw_norm:
        return False
    if kw_norm.isascii() and len(kw_norm) <= 3:
        # Very short English keywords (e.g. "ac", "oil") must match a whole word, not a substring.
        return kw_norm in tokens
    if kw_norm in norm_query:
        return True
    kw_no_apos = kw_norm.replace("'", "")
    if kw_no_apos in norm_query.replace("'", ""):
        return True
    kw_parts = kw_no_apos.split()
    if not kw_no_apos.isascii():
        # Lao keywords: substring match only (Lao is written without spaces, stemming doesn't apply).
        return False
    if len(kw_parts) == 1:
        stem = kw_parts[0][:4] if len(kw_parts[0]) >= 5 else kw_parts[0]
        for tok in tokens:
            if tok == kw_parts[0] or (len(stem) >= 4 and tok.startswith(stem)):
                return True
    else:
        # All parts present in tokens
        if all(
            any(tok == part or (len(part) >= 5 and tok.startswith(part[:4])) for tok in tokens)
            for part in kw_parts
        ):
            return True
    return False


def diagnose_problem(db: Session, problem_query: str, category_id: int | None = None) -> tuple[DiagnosisResult, dict[int, int], list[str]]:
    """
    Analyze user's plain-language problem description.
    Returns (DiagnosisResult, matched_category_weights, extracted_tokens).
    """
    norm_query = normalize_text(problem_query)
    tokens = extract_tokens(problem_query)

    category_weights: dict[int, int] = {}
    symptom_labels: list[str] = []
    advice_hints: list[str] = []

    if category_id is not None:
        category_weights[category_id] = 60

    if norm_query:
        all_keywords = db.query(ProblemKeyword).all()
        for pk in all_keywords:
            if category_id is not None and pk.category_id != category_id:
                continue
            if token_matches_keyword(tokens, norm_query, pk.keyword):
                weight = 40 if len(pk.keyword.split()) > 1 else 25
                category_weights[pk.category_id] = category_weights.get(pk.category_id, 0) + weight
                if pk.symptom_label not in symptom_labels:
                    symptom_labels.append(pk.symptom_label)
                if pk.advice_hint not in advice_hints:
                    advice_hints.append(pk.advice_hint)

        # Also check category name/description directly
        categories = db.query(Category).all()
        for cat in categories:
            if category_id is not None and cat.id != category_id:
                continue
            cat_text = normalize_text(f"{cat.name} {cat.description}")
            for tok in tokens:
                if tok in cat_text:
                    category_weights[cat.id] = category_weights.get(cat.id, 0) + 20

    matched_cat_models: list[Category] = []
    if category_weights:
        sorted_cat_ids = sorted(category_weights.keys(), key=lambda cid: category_weights[cid], reverse=True)
        cat_map = {
            c.id: c
            for c in db.query(Category).filter(Category.id.in_(sorted_cat_ids)).all()
        }
        matched_cat_models = [cat_map[cid] for cid in sorted_cat_ids if cid in cat_map]

    matched_cat_outs = [
        CategoryOut(
            id=c.id,
            name=c.name,
            slug=c.slug,
            icon=c.icon,
            color=c.color,
            description=c.description,
            shop_count=0,
        )
        for c in matched_cat_models
    ]

    diagnosis = DiagnosisResult(
        query=problem_query.strip(),
        matched_categories=matched_cat_outs,
        symptom_labels=symptom_labels[:4],
        advice_hints=advice_hints[:3],
        notification_summary="",
    )
    return diagnosis, category_weights, tokens


def score_shop_for_problem(
    shop: Shop,
    problem_query: str,
    category_weights: dict[int, int],
    tokens: list[str],
) -> tuple[int, list[str]]:
    """Return (match_score, matched_reasons) for a single approved shop."""
    if not problem_query.strip() and not category_weights:
        return 10, []

    score = 0
    reasons: list[str] = []

    if shop.category_id in category_weights:
        score += min(60, 30 + category_weights[shop.category_id] // 2)
        reasons.append(f"ແນະນຳ: {shop.category.name}")

    tags_list = [t.strip() for t in shop.problem_tags.split(",") if t.strip()]
    norm_query = normalize_text(problem_query)

    matched_tags: list[str] = []
    for tag in tags_list:
        if token_matches_keyword(tokens, norm_query, tag):
            score += 25
            matched_tags.append(tag)
        else:
            tag_norm = normalize_text(tag)
            for tok in tokens:
                if len(tok) >= 3 and tok in tag_norm:
                    score += 15
                    matched_tags.append(tag)
                    break

    if matched_tags:
        dedup_tags = list(dict.fromkeys(matched_tags))[:3]
        reasons.append(f"ແກ້ໄຂໄດ້: {', '.join(dedup_tags)}")

    searchable_text = normalize_text(f"{shop.name} {shop.description}")
    text_hits = [tok for tok in tokens if len(tok) >= 3 and tok in searchable_text]
    if text_hits:
        score += min(25, len(text_hits) * 10)
        if not matched_tags and shop.category_id not in category_weights:
            reasons.append(f"ກ່ຽວຂ້ອງກັບ: {', '.join(text_hits[:2])}")

    is_urgent = any(w in URGENT_WORDS for w in tokens) or any(p in norm_query for p in URGENT_PHRASES_LO)
    if shop.is_emergency_24h and is_urgent:
        score += 20
        reasons.append("ບໍລິການສຸກເສີນ 24 ຊົ່ວໂມງ")

    return score, reasons

