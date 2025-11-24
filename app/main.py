from fastapi import FastAPI, Request, HTTPException
from .config import EMAIL, SECRET
from .solver import solve_once
import httpx
import time

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Quiz solver is running"}

@app.post("/")
async def entry(req: Request):
    start = time.time()

    data = await req.json()

    if data.get("secret") != SECRET:
        raise HTTPException(403, "Forbidden")

    next_url = data.get("url")
    if not next_url:
        raise HTTPException(400, "Missing url")

    while next_url and time.time() - start < 170:
        submit_url, answer = await solve_once(next_url)

        payload = {
            "email": EMAIL,
            "secret": SECRET,
            "url": next_url,
            "answer": answer
        }

        async with httpx.AsyncClient() as client:
            r = await client.post(submit_url, json=payload)
            out = r.json()

        next_url = out.get("url")

    return {"completed": True}
