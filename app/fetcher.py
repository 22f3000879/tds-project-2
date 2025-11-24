import httpx
from .config import AIPIPE_TOKEN, AIPIPE_BROWSER

async def fetch_page(url: str) -> str:
    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "url": url,
        "javascript": True,
        "wait_for": 2500
    }

    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(AIPIPE_BROWSER, json=payload, headers=headers)
        res.raise_for_status()
        return res.json()["content"]
