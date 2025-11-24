from .fetcher import fetch_page
from .llm import ask_llm
from .parser import build_prompt
import json, re

async def solve_once(url: str):
    html = await fetch_page(url)
    prompt = build_prompt(html)
    llm_output = await ask_llm(prompt)

    # Debug
    print("LLM OUTPUT RAW:", llm_output)

    # Extract JSON from messy output
    try:
        return_data = json.loads(llm_output)
    except:
        m = re.search(r"\[.*\]", llm_output, re.S)
        if not m:
            raise ValueError("LLM did not return JSON at all.")
        return_data = json.loads(m.group(0))

    if not return_data:
        raise ValueError("LLM returned an empty list.")

    item = return_data[0]
    return item["submit_url"], item["answer"]
