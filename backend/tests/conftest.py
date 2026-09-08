"""Shared test fixtures.

Tests that need a real database are marked ``@pytest.mark.integration`` and are
deselected by default (``-m "not integration"``), so the default suite runs with no
Docker, no Postgres, and no Floci.
"""

from collections.abc import AsyncIterator, Iterator

import pytest
from httpx import ASGITransport, AsyncClient

from tournament.config import get_settings
from tournament.main import create_app


@pytest.fixture(autouse=True)
def _clear_settings_cache() -> Iterator[None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """HTTP client wired straight to the ASGI app — no network, no running server."""
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
