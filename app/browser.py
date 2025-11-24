import httpx
from .config import AIPIPE_TOKEN, AIPIPE_API

async def fetch_page(url: str) -> str:
    print("DEBUG:", AIPIPE_API, AIPIPE_TOKEN)
    """
    Fetch fully rendered HTML using AiPipe Browser Engine.
    """
    payload = {
        "url": url,
        "javascript": True,
        "wait_for": 2000
    }

    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(AIPIPE_API, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()["content"]
