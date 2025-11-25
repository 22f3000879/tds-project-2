from .config import AIPIPE_TOKEN, AIPIPE_BASE
import httpx
import json

async def llm_solve(question: str, data: str) -> str:
    system_prompt = "You are a highly accurate data analyst. Always return only the final answer."
    user_prompt = f"Question:\n{question}\n\nData:\n{data}\n\nReturn only the result."

    payload = {
        "model": "gpt-5-nano",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    }

    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(AIPIPE_BASE, json=payload, headers=headers)
        r.raise_for_status()

    return r.json()["choices"][0]["message"]["content"].strip()
