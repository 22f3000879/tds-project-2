from fastapi import FastAPI, HTTPException, Request
from .config import SECRET, EMAIL
from .solver import solve_once
import httpx
import time

app = FastAPI()

@app.post("/")
async def entry(req: Request):
    start = time.time()
    try:
        data = await req.json()
    except:
        raise HTTPException(400, "Invalid JSON")

    if data.get("secret") != SECRET:
        raise HTTPException(403, "Forbidden")

    url = data.get("url")
    if not url:
        raise HTTPException(400, "Missing url")

    next_url = url

    # Up to 3 minutes to solve chain
    while next_url and time.time() - start < 170:
        submit_url, answer = await solve_once(next_url)

        payload = {
            "email": EMAIL,
            "secret": SECRET,
            "url": next_url,
            "answer": answer
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(submit_url, json=payload)
        res = resp.json()

        next_url = res.get("url")

    return {"done": True}
