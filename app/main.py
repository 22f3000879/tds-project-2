from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .config import SECRET
from .fetcher import fetch_raw
from .extractor import extract_payload
from .solver import solve_question
from .submitter import submit_answer

app = FastAPI()

@app.post("/")
async def entry(request: Request):
    try:
        payload = await request.json()
    except:
        return JSONResponse({"error": "invalid json"}, 400)

    if payload.get("secret") != SECRET:
        return JSONResponse({"error": "forbidden"}, 403)

    quiz_url = payload.get("url")
    if not quiz_url:
        return JSONResponse({"error": "url missing"}, 400)

    results = []

    # chain until no next url
    current = quiz_url
    while current:
        html = await fetch_raw(current)
        decoded_html, data = extract_payload(html)
        answer = await solve_question(decoded_html, data)
        submit_url = data["submit_url"]

        res = await submit_answer(submit_url, current, answer)
        results.append({
            "url": current,
            "answer": answer,
            "result": res
        })

        current = res.get("url")  # next quiz page or None

    return {"done": True, "results": results}
