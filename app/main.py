from fastapi import FastAPI, Request
from .config import SECRET
from .solver import solve_once

app = FastAPI()

@app.post("/")
async def entry(request: Request):
    try:
        data = await request.json()
    except:
        return {"error": "invalid json"}, 400

    if data.get("secret") != SECRET:
        return {"error": "forbidden"}, 403

    url = data.get("url")
    if not url:
        return {"error": "missing url"}, 400

    result = await solve_once(url)
    return result
