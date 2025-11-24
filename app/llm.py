import httpx
from .config import AIPIPE_TOKEN, AIPIPE_LLM

async def ask_llm(prompt: str):
    payload = {
        "model": "gpt-4o-mini",  
        "messages": [
            {"role": "system", "content": "You are a smart assistant extracting quiz answers."},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(AIPIPE_LLM, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
