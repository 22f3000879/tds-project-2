import httpx

async def submit_answer(submit_url: str, payload: dict):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(submit_url, json=payload)
        r.raise_for_status()
        return r.json()
