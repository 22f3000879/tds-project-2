import httpx

client = httpx.AsyncClient(timeout=20)

async def submit_answer(submit_url: str, email: str, secret: str, quiz_url: str, answer):
    payload = {
        "email": email,
        "secret": secret,
        "url": quiz_url,
        "answer": answer
    }
    r = await client.post(submit_url, json=payload)
    r.raise_for_status()
    return r.json()
