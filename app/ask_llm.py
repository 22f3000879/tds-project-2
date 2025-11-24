import httpx
from .config import AIPIPE_TOKEN, AIPIPE_BASE

async def ask_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-5-nano",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(AIPIPE_BASE, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()

    # AiPipe returns:
    # "content": [{ "text": "..."}]
    chunks = data["choices"][0]["message"]["content"]

    # Join all pieces into a single string
    text = "".join(chunk.get("text", "") for chunk in chunks)

    return text.strip()
