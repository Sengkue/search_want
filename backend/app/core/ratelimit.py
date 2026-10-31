"""Thread-safe in-memory sliding-window rate limiter for authentication & sensitive endpoints."""

from collections import defaultdict, deque
from threading import Lock
import time

from fastapi import HTTPException, Request, status

_lock = Lock()
_buckets: dict[str, deque[float]] = defaultdict(deque)


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def enforce_rate_limit(
    bucket: str,
    key: str,
    max_requests: int,
    window_seconds: int,
    detail: str = "ທ່ານສົ່ງຄຳຂໍຫຼາຍເກີນໄປ ກະລຸນາລໍຖ້າສັກຄູ່ແລ້ວລອງໃໝ່.",
) -> None:
    now = time.monotonic()
    cutoff = now - window_seconds
    composite_key = f"{bucket}:{key}"

    with _lock:
        timestamps = _buckets[composite_key]
        while timestamps and timestamps[0] <= cutoff:
            timestamps.popleft()

        if len(timestamps) >= max_requests:
            retry_after = max(1, int(window_seconds - (now - timestamps[0])))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=detail,
                headers={"Retry-After": str(retry_after)},
            )
        timestamps.append(now)


def clear_rate_limit_key(bucket: str, key: str) -> None:
    composite_key = f"{bucket}:{key}"
    with _lock:
        _buckets.pop(composite_key, None)


def reset_all_rate_limits() -> None:
    with _lock:
        _buckets.clear()
