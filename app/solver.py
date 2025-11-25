from .fetcher import fetch_page
from .dom_llm import llm_extract
from .quiz_llm import llm_solve
from .submit import submit_answer

async def solve_once(url: str):
    html = await fetch_page(url)

    info = await llm_extract(html)

    if "raw" in info:
        raise ValueError("LLM failed to parse quiz HTML.")

    question = info.get("question", "")
    data_url = info.get("data_url", "")
    submit_url = info.get("submit_url")

    if not submit_url:
        raise ValueError("No submit URL found.")

    # Download data (csv, pdf, anything as text)
    data = ""
    if data_url:
        async_data = await fetch_page(data_url)
        data = async_data

    # Solve using LLM
    answer = await llm_solve(question, data)

    return submit_url, answer
