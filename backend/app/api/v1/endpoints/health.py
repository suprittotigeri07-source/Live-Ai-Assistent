from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.core.settings import settings

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health():
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
    )