import pytest

from src.client_for3party.client import ClientBase


@pytest.mark.asyncio
async def test_client_base():
    async with ClientBase('https://google.com') as client:
        async with client.session.get(f'{client.base_url}/') as resp:
            rs = await client.is_success(resp)
    assert isinstance(rs, bool)
