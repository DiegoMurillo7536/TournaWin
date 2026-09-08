"""Liveness probe must answer without any database."""

from httpx import AsyncClient


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "environment": "local"}


async def test_openapi_schema_is_generated(client: AsyncClient) -> None:
    """The OpenAPI doc is the frontend's contract, so it must always build."""
    response = await client.get("/openapi.json")

    assert response.status_code == 200
    assert "/health" in response.json()["paths"]
