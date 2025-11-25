import httpx
from .config import EMAIL, SECRET

async def submit_answer(url, quiz_url, answer):
    payload = {
        "email": EMAIL,
        "secret": SECRET,
        "url": quiz_url,
        "answer": answer
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        return r.json()
