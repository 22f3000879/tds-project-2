import httpx

async def submit_answer(url: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        return r.json()
