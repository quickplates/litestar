from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient


async def test_get(client: AsyncTestClient) -> None:
    """Test if GET / returns correct response."""

    async with client as client:
        response = await client.get("/")
        assert response.status_code == HTTP_200_OK
        assert response.json() == {"foo": "bar"}
