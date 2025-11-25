import json
from .fetcher import fetch_html, fetch_file
from .parser import parse_quiz
from .extractor import extract_answer
from .llm import ask_llm

async def solve_once(url: str):
    html = await fetch_html(url)
    parsed = parse_quiz(html)

    instructions = parsed["instructions"]
    file_url = parsed["file_url"]
    submit_url = parsed["submit_url"]

    file_bytes = None
    if file_url:
        file_bytes = await fetch_file(file_url)

    # Try rule-based extraction first
    answer = extract_answer(instructions, file_bytes)

    # If rules failed → ask LLM to compute
    if answer is None:
        prompt = f"""
You are a data assistant. A quiz question says:

{instructions}

Extract the correct answer ONLY.
If a file was downloaded, here is extracted text for reference:

{file_bytes[:500] if file_bytes else 'No file'}

Return ONLY a JSON like: {{"answer": VALUE}}
"""
        llm_out = await ask_llm(prompt)
        try:
            answer = json.loads(llm_out)["answer"]
        except:
            answer = llm_out  # fallback

    return submit_url, answer
