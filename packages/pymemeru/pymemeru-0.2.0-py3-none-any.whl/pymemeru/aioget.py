import httpx


async def aioget(url, params={}, timeout=10):
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params, timeout=timeout)
        return r.text
