from fastapi import FastAPI, Request, HTTPException
from app.config import SECRET, EMAIL
from app.solver import solve_once
from app.submit import submit_answer

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "ok", "message": "TDS Project 2 Running"}

@app.post("/")
async def endpoint(request: Request):
    try:
        payload = await request.json()
    except:
        raise HTTPException(400, "Invalid JSON")

    if payload.get("secret") != SECRET:
        raise HTTPException(403, "Forbidden")

    quiz_url = payload.get("url")
    if not quiz_url:
        raise HTTPException(400, "Missing quiz URL")

    # Solve first question
    submit_url, answer = await solve_once(quiz_url, EMAIL, SECRET)

    result = await submit_answer(submit_url, EMAIL, SECRET, quiz_url, answer)

    # Loop if more questions exist
    while result.get("url"):
        next_url = result["url"]
        submit_url, answer = await solve_once(next_url, EMAIL, SECRET)
        result = await submit_answer(submit_url, EMAIL, SECRET, next_url, answer)

    return result
