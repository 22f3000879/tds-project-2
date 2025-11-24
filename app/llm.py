import httpx
import os

# Ensure you have AIPROXY_TOKEN set in your Render Environment Variables
TOKEN = os.getenv("AIPROXY_TOKEN") 

async def llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Solve precisely. Output only final answer."},
            {"role": "user", "content": prompt}
        ]
    }
    
    # Use the course proxy or official OpenAI URL
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
