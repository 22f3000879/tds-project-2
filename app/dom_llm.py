from .config import AIPIPE_TOKEN, AIPIPE_BASE
import httpx
import json

async def llm_extract(html: str) -> dict:
    system_prompt = "You are a precise DOM interpreter. Extract quiz instructions accurately."
    user_prompt = f"HTML:\n{html}\n\nExtract: question text, required steps, data URLs, submit URL."

    payload = {
        "model": "gpt-5-nano",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(AIPIPE_BASE, json=payload, headers=headers)
        r.raise_for_status()

    text = r.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(text)
    except:
        return {"raw": text}
