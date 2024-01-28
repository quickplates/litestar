import pytest
from litestar.status_codes import HTTP_204_NO_CONTENT
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio(scope="session")
async def test_get(client: AsyncTestClient) -> None:
    """Test if GET /ping returns correct response."""

    response = await client.get("/ping")
    assert response.status_code == HTTP_204_NO_CONTENT
    assert len(response.content) == 0
