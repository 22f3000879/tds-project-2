import httpx

async def fetch_raw(url: str) -> str:
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text
