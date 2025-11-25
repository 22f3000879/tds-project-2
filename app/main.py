from fastapi import FastAPI, Request
import httpx
from .config import SECRET, EMAIL
from .solver import solve_once

app = FastAPI()

@app.post("/")
async def entry(request: Request):
    try:
        data = await request.json()
    except:
        return {"error": "invalid JSON"}, 400

    if data.get("secret") != SECRET:
        return {"error": "forbidden"}, 403

    next_url = data.get("url")
    if not next_url:
        return {"error": "Missing URL"}, 400

    # Solve loop (multiple quiz steps)
    current_url = next_url
    last_status = None

    async with httpx.AsyncClient(timeout=60) as client:
        for _ in range(10):      # max 10 tasks per chain
            submit_url, answer = await solve_once(current_url)

            payload = {
                "email": EMAIL,
                "secret": SECRET,
                "url": current_url,
                "answer": answer
            }

            r = await client.post(submit_url, json=payload)
            r.raise_for_status()
            result = r.json()
            last_status = result

            if "url" in result and result["url"]:
                current_url = result["url"]
                continue
            break

    return last_status
