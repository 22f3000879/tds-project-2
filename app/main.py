from fastapi import FastAPI, Request, HTTPException
import time
from .config import SECRET, EMAIL
from .solver import solve_once
from .submit import submit_answer

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LLM Quiz Solver running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/")
async def endpoint(req: Request):
    start = time.time()

    try:
        data = await req.json()
    except:
        raise HTTPException(400, "Invalid JSON")

    if data.get("secret") != SECRET:
        raise HTTPException(403, "Forbidden")

    quiz_url = data.get("url")
    if not quiz_url:
        raise HTTPException(400, "Missing quiz URL")

    next_url = quiz_url

    while next_url and time.time() - start < 170:
        submit_url, answer = await solve_once(next_url)

        resp = await submit_answer(submit_url, next_url, answer)

        next_url = resp.get("url")

    return {"done": True}
