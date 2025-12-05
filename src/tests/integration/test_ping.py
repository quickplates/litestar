import pytest
from litestar.status_codes import HTTP_204_NO_CONTENT
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio(loop_scope="session")
async def test_get(client: AsyncTestClient) -> None:
    """Test if GET /ping returns correct response."""
    response = await client.get("/ping")

    status = response.status_code
    assert status == HTTP_204_NO_CONTENT

    headers = response.headers
    assert "Cache-Control" in headers
    assert headers["Cache-Control"] == "no-store"

    content = response.content
    assert len(content) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_head(client: AsyncTestClient) -> None:
    """Test if HEAD /ping returns correct response."""
    response = await client.head("/ping")

    status = response.status_code
    assert status == HTTP_204_NO_CONTENT

    headers = response.headers
    assert "Cache-Control" in headers
    assert headers["Cache-Control"] == "no-store"

    content = response.content
    assert len(content) == 0
