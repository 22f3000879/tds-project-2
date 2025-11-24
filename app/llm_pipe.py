import httpx
import os

AIPIPE_API_KEY = os.getenv("AIPIPE_API_KEY")

async def ask_llm(system_prompt: str, user_prompt: str):
    headers = {
        "Authorization": f"Bearer {AIPIPE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",     # recommended for reasoning + speed
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://aipipe.org/api/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
