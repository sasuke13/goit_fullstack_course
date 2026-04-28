from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="Health check")
async def healthcheck() -> dict[str, str]:
    """Return a simple status response for uptime checks."""
    return {"status": "ok"}
