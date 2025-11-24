from .fetcher import fetch_page
from .llm import ask_llm
from .parser import build_prompt
import json

async def solve_once(url: str):
    html = await fetch_page(url)

    prompt = build_prompt(html)
    llm_output = await ask_llm(prompt)

    try:
        data = json.loads(llm_output)
    except:
        raise ValueError("LLM returned invalid JSON: " + llm_output)

    item = data[0]  # one question at a time

    return item["submit_url"], item["answer"]
