import httpx
import os

def get_key():
    key = os.getenv("AI_PIPE")
    if not key:
        raise ValueError("AI_PIPE environment variable missing.")
    return key

async def ask_llm(system_prompt: str, user_prompt: str):
    headers = {
        "Authorization": f"Bearer {get_key()}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://aipipe.org/api/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )

    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
