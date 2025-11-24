import httpx
from .config import AIPIPE_TOKEN, AIPIPE_LLM

async def llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Solve precisely. Output only final answer."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(AIPIPE_LLM, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
