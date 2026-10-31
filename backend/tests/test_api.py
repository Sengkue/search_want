import os
import tempfile
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure isolated test SQLite database before importing app modules
_tmp_db_fd, _tmp_db_path = tempfile.mkstemp(suffix=".db")
os.close(_tmp_db_fd)
os.environ["SEARCH_WANT_DATABASE_URL"] = f"sqlite:///{_tmp_db_path}"

from app.core.config import settings  # noqa: E402
from app.core.ratelimit import reset_all_rate_limits  # noqa: E402
from app.db.database import Base, get_db  # noqa: E402
from app.db.seed import seed_initial_data  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    reset_all_rate_limits()
    test_fd, test_path = tempfile.mkstemp(suffix=".db")
    os.close(test_fd)
    test_engine = create_engine(
        f"sqlite:///{test_path}", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as tc:
        yield tc

    app.dependency_overrides.clear()
    test_engine.dispose()
    if os.path.exists(test_path):
        os.remove(test_path)


def test_health_and_seeded_categories(client: TestClient) -> None:
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    cats = client.get("/api/categories")
    assert cats.status_code == 200
    cat_list = cats.json()
    assert len(cat_list) >= 8
    slugs = {c["slug"] for c in cat_list}
    assert "car-auto-repair" in slugs
    assert "towing-roadside" in slugs

    symptoms = client.get("/api/categories/symptoms")
    assert symptoms.status_code == 200
    assert len(symptoms.json()) >= 15


def test_problem_search_matches_car_trouble_and_hides_pending_shops(client: TestClient) -> None:
    resp = client.get(
        "/api/shops/nearby",
        params={
            "problem": "my car have problem something I do not know how to fix engine won't start",
            "lat": 17.9757,
            "lng": 102.6331,
            "radius_km": 15.0,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_found"] >= 2

    # Diagnosis should match automotive categories and provide safety/diagnostic hints
    matched_slugs = {c["slug"] for c in data["diagnosis"]["matched_categories"]}
    assert "car-auto-repair" in matched_slugs
    assert len(data["diagnosis"]["advice_hints"]) >= 1
    assert "ກມ." in data["diagnosis"]["notification_summary"]

    # Every returned shop MUST be APPROVED and sorted by distance ascending for top matches
    shops = data["shops"]
    assert all(s["status"] == "APPROVED" for s in shops)
    distances = [s["distance_km"] for s in shops if s["match_score"] >= 30]
    assert distances == sorted(distances)


def test_full_shop_submission_and_admin_approval_lifecycle(client: TestClient) -> None:
    # 1. Register a brand new user
    reg = client.post(
        "/api/auth/register",
        json={
            "email": "mechanic_joe@example.com",
            "password": "password123",
            "full_name": "Mechanic Joe",
            "phone": "+66 89-000-9999",
        },
    )
    assert reg.status_code == 201
    owner_token = reg.json()["access_token"]
    owner_headers = {"Authorization": f"Bearer {owner_token}"}

    # 2. Get Car & Auto Repair category ID
    cats = client.get("/api/categories").json()
    car_cat = next(c for c in cats if c["slug"] == "car-auto-repair")

    # 3. Submit a new shop right next to user location (status must start PENDING)
    create_resp = client.post(
        "/api/shops",
        headers=owner_headers,
        json={
            "category_id": car_cat["id"],
            "name": "Joe Roadside Car Clinic",
            "description": "Fixes cars that won't start, alternator & starter motor repairs.",
            "problem_tags": "car won't start, starter motor, alternator, check engine",
            "phone": "+66 89-000-9999",
            "address": "12 Roadside Soi 1",
            "latitude": 17.9759,
            "longitude": 102.6333,
            "opening_hours": "08:00 - 21:00",
            "is_emergency_24h": True,
        },
    )
    assert create_resp.status_code == 201
    created_shop = create_resp.json()
    shop_id = created_shop["id"]
    assert created_shop["status"] == "PENDING"

    # 4. Verify PENDING shop is NOT visible in public nearby search yet
    nearby_before = client.get(
        "/api/shops/nearby",
        params={"problem": "car won't start", "lat": 17.9757, "lng": 102.6331, "radius_km": 10},
    ).json()
    assert all(s["id"] != shop_id for s in nearby_before["shops"])

    # 5. Non-admin cannot approve their own shop
    forbidden = client.post(
        f"/api/admin/shops/{shop_id}/decision",
        headers=owner_headers,
        json={"action": "APPROVE"},
    )
    assert forbidden.status_code == 403

    # 6. Admin logs in and sees the pending shop + notification
    admin_login = client.post(
        "/api/auth/login",
        json={"email": "admin@searchwant.com", "password": "admin123"},
    )
    assert admin_login.status_code == 200
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    stats = client.get("/api/admin/stats", headers=admin_headers).json()
    assert stats["pending_count"] >= 1

    # 7. Admin first rejects with feedback note
    reject_resp = client.post(
        f"/api/admin/shops/{shop_id}/decision",
        headers=admin_headers,
        json={"action": "REJECT", "note": "Please include house number in address."},
    )
    assert reject_resp.status_code == 200
    assert reject_resp.json()["status"] == "REJECTED"

    # Owner checks notifications & edits shop to resubmit
    owner_notifs = client.get("/api/notifications", headers=owner_headers).json()
    assert any(n["notif_type"] == "SHOP_REJECTED" for n in owner_notifs)

    resubmit_resp = client.put(
        f"/api/shops/{shop_id}",
        headers=owner_headers,
        json={
            "category_id": car_cat["id"],
            "name": "Joe Roadside Car Clinic",
            "description": "Fixes cars that won't start, alternator & starter motor repairs.",
            "problem_tags": "car won't start, starter motor, alternator, check engine",
            "phone": "+66 89-000-9999",
            "address": "House #99, 12 Roadside Soi 1",
            "latitude": 17.9759,
            "longitude": 102.6333,
            "opening_hours": "08:00 - 21:00",
            "is_emergency_24h": True,
        },
    )
    assert resubmit_resp.status_code == 200
    assert resubmit_resp.json()["status"] == "PENDING"

    # 8. Admin approves the resubmitted shop ("I just approve only")
    approve_resp = client.post(
        f"/api/admin/shops/{shop_id}/decision",
        headers=admin_headers,
        json={"action": "APPROVE", "note": "Verified map location and address!"},
    )
    assert approve_resp.status_code == 200
    assert approve_resp.json()["status"] == "APPROVED"

    # 9. Shop IMMEDIATELY appears as the closest shop (~0.03 km away!) in nearby search
    nearby_after = client.get(
        "/api/shops/nearby",
        params={"problem": "car won't start", "lat": 17.9757, "lng": 102.6331, "radius_km": 10},
    ).json()
    found_ids = [s["id"] for s in nearby_after["shops"]]
    assert shop_id in found_ids
    assert nearby_after["shops"][0]["id"] == shop_id

    # 10. Owner received SHOP_APPROVED notification
    owner_notifs_after = client.get("/api/notifications", headers=owner_headers).json()
    assert any(n["notif_type"] == "SHOP_APPROVED" for n in owner_notifs_after)


def test_lao_language_problem_search(client: TestClient) -> None:
    """A Lao-language problem (no spaces between words) must match Lao categories & shops."""
    resp = client.get(
        "/api/shops/nearby",
        params={
            "problem": "ລົດຂອງຂ້ອຍສະຕາດບໍ່ຕິດ ຕ້ອງການຄົນຊ່ວຍດ່ວນ",
            "lat": 17.9757,
            "lng": 102.6331,
            "radius_km": 15,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_found"] >= 2
    matched_slugs = {c["slug"] for c in data["diagnosis"]["matched_categories"]}
    assert "car-auto-repair" in matched_slugs
    assert data["diagnosis"]["symptom_labels"]
    assert all(s["status"] == "APPROVED" for s in data["shops"])

    # Categories & seeded shops are returned in Lao
    cats = client.get("/api/categories").json()
    car = next(c for c in cats if c["slug"] == "car-auto-repair")
    assert car["name"] == "ສ້ອມແປງລົດ ແລະ ອູ່ລົດ"


def test_seed_nearby_requires_admin_and_blocks_production(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = {"latitude": 35.6762, "longitude": 139.6503, "area_name": "Tokyo Test"}

    # 1. Anonymous visitor cannot pollute database with demo shops
    anon_resp = client.post("/api/shops/seed-nearby", json=payload)
    assert anon_resp.status_code == 401

    # 2. Regular customer cannot seed demo shops
    user_login = client.post(
        "/api/auth/login",
        json={"email": "user@searchwant.com", "password": "user123"},
    )
    user_headers = {"Authorization": f"Bearer {user_login.json()['access_token']}"}
    user_resp = client.post("/api/shops/seed-nearby", headers=user_headers, json=payload)
    assert user_resp.status_code == 403

    # 3. Admin/Super Admin can seed demo shops ONLY when DEMO_MODE is True
    admin_login = client.post(
        "/api/auth/login",
        json={"email": "admin@searchwant.com", "password": "admin123"},
    )
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    seed_resp = client.post("/api/shops/seed-nearby", headers=admin_headers, json=payload)
    assert seed_resp.status_code == 200
    assert seed_resp.json()["created_count"] >= 7

    nearby_tokyo = client.get(
        "/api/shops/nearby",
        params={"problem": "flat tire", "lat": 35.6762, "lng": 139.6503, "radius_km": 10},
    ).json()
    assert nearby_tokyo["total_found"] >= 1

    # 4. In Production (DEMO_MODE=False), even Super Admin is blocked from injecting fake demo shops
    monkeypatch.setattr(settings, "DEMO_MODE", False)
    prod_seed = client.post("/api/shops/seed-nearby", headers=admin_headers, json=payload)
    assert prod_seed.status_code == 403


def test_mobile_apk_download_endpoints(client: TestClient) -> None:
    info = client.get("/api/app/apk-info")
    assert info.status_code == 200
    payload = info.json()
    assert payload["filename"] == "Search-Want.apk"
    if payload["available"]:
        assert payload["size_mb"] > 1.0
        dl = client.get("/api/app/apk")
        assert dl.status_code == 200
        assert dl.headers["content-type"] == "application/vnd.android.package-archive"
        assert "Search-Want.apk" in dl.headers.get("content-disposition", "")


def test_adsense_config_admin_update_and_ads_txt(client: TestClient) -> None:
    # 1. Public default AdSense config starts enabled with configured Publisher ID
    initial = client.get("/api/adsense/config")
    assert initial.status_code == 200
    cfg = initial.json()
    assert cfg["enabled"] is True
    assert cfg["client_id"] == "ca-pub-4990570878383229"

    # Default /ads.txt returns official Google verification line
    ads_txt_before = client.get("/ads.txt")
    assert ads_txt_before.status_code == 200
    assert (
        ads_txt_before.text.strip()
        == "google.com, pub-4990570878383229, DIRECT, f08c47fec0942fa0"
    )

    # 2. Non-admin cannot modify AdSense settings
    reg = client.post(
        "/api/auth/register",
        json={
            "email": "regular_viewer@example.com",
            "password": "password123",
            "full_name": "Regular Viewer",
        },
    )
    user_headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
    forbidden = client.put(
        "/api/admin/adsense",
        headers=user_headers,
        json={"enabled": False},
    )
    assert forbidden.status_code == 403

    # 3. Admin logs in, validates invalid ID gets 422, then saves valid Publisher ID & Slots
    admin_login = client.post(
        "/api/auth/login",
        json={"email": "admin@searchwant.com", "password": "admin123"},
    )
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    bad_resp = client.put(
        "/api/admin/adsense",
        headers=admin_headers,
        json={"client_id": "invalid-pub-id"},
    )
    assert bad_resp.status_code == 422

    # Supports short pub-XXXXXXXXXXXXXXXX normalization to ca-pub-XXXXXXXXXXXXXXXX
    update_resp = client.put(
        "/api/admin/adsense",
        headers=admin_headers,
        json={
            "enabled": True,
            "client_id": "pub-1234567890123456",
            "slot_infeed": "1122334455",
            "slot_banner": "6677889900",
            "auto_ads": True,
            "test_mode": False,
        },
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["client_id"] == "ca-pub-1234567890123456"
    assert updated["publisher_id"] == "pub-1234567890123456"
    assert updated["slot_infeed"] == "1122334455"
    assert updated["slot_banner"] == "6677889900"
    assert updated["test_mode"] is False

    # 4. /ads.txt immediately reflects Google's official format
    ads_txt_after = client.get("/ads.txt")
    assert ads_txt_after.status_code == 200
    assert (
        ads_txt_after.text.strip()
        == "google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0"
    )



