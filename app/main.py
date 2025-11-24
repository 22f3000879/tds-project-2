from fastapi import FastAPI, HTTPException, Request
from app.config import SECRET
from app.solver import solve_quiz
import httpx, asyncio

app = FastAPI()

@app.post("/")
async def root(req: Request):
    try:
        data = await req.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if "secret" not in data:
        raise HTTPException(status_code=400, detail="Missing secret")

    if data["secret"] != SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    if "url" not in data:
        raise HTTPException(status_code=400, detail="Missing url")

    quiz_url = data["url"]
    submit_url, payload = await solve_quiz(quiz_url)

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(submit_url, json=payload)

    result = r.json()

    # If new URL returned → chain
    if "url" in result and result["url"]:
        await solve_quiz(result["url"])

    return {"received": True, "submitted": result}
