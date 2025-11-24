from .fetcher import fetch_page
from .llm import ask_llm
from .parser import build_prompt
import json

async def solve_once(url: str):
    html = await fetch_page(url)

    prompt = build_prompt(html)
    llm_output = await ask_llm(prompt)

    # Debug print for Render logs
    print("LLM OUTPUT:", llm_output)

    try:
        data = json.loads(llm_output)
    except Exception:
        raise ValueError("LLM returned invalid JSON:\n" + llm_output)

    if not data:
        raise ValueError("LLM returned empty list:\n" + llm_output)

    item = data[0]

    if "submit_url" not in item or "answer" not in item:
        raise ValueError("Missing fields in LLM output:\n" + llm_output)

    return item["submit_url"], item["answer"]
