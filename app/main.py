from fastapi import FastAPI, Request, HTTPException
import time

from .config import EMAIL, SECRET
from .solver import solve_once
from .submit import submit_answer

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running", "email": EMAIL}


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
        raise HTTPException(400, "Missing URL")

    next_url = quiz_url

    # 3-minute evaluation loop
    while next_url and time.time() - start < 170:
        submit_url, answer = await solve_once(next_url, EMAIL, SECRET)

        payload = {
            "email": EMAIL,
            "secret": SECRET,
            "url": next_url,
            "answer": answer,
        }

        result = await submit_answer(submit_url, payload)

        next_url = result.get("url")

    return {"done": True}
