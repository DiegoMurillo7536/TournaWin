"""Liveness and readiness probes.

``/health`` must not touch the database: it answers "is this process alive".
``/health/ready`` answers "can this process serve traffic", which does require the DB.
"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from tournament.api.deps import SessionDep, SettingsDep
from tournament.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(settings: SettingsDep) -> HealthResponse:
    return HealthResponse(status="ok", environment=settings.environment)


@router.get("/health/ready")
async def ready(session: SessionDep) -> ReadinessResponse:
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:  # a probe reports any failure as not-ready
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="database unavailable",
        ) from exc
    return ReadinessResponse(status="ready", database="up")
