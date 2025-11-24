from fastapi import FastAPI, Request, HTTPException
from .config import EMAIL, SECRET
from .solver import solve_once
import time, httpx

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Quiz solver is running"}

@app.post("/")
async def entry(req: Request):
    start = time.time()

    try:
        payload = await req.json()
    except:
        raise HTTPException(400, "Invalid JSON")

    if payload.get("secret") != SECRET:
        raise HTTPException(403, "Forbidden")

    next_url = payload.get("url")
    if not next_url:
        raise HTTPException(400, "Missing url")

    while next_url and time.time() - start < 165:
        submit_url, answer = await solve_once(next_url)

        submission = {
            "email": EMAIL,
            "secret": SECRET,
            "url": next_url,
            "answer": answer
        }

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(submit_url, json=submission)
            result = r.json()

        next_url = result.get("url")

    return {"completed": True}
