from .fetcher import fetch_page, clean_html
from .dom_llm import extract_quiz_info
from .quiz_llm import solve_task
from .utils import download_file, extract_pdf_tables
import json
import os

async def solve_once(url: str, email: str, secret: str):
    raw_html = await fetch_page(url)
    text = clean_html(raw_html)

    quiz = await extract_quiz_info(text)
    if not quiz:
        raise ValueError("LLM failed to interpret quiz page.")

    submit_url = quiz["submit_url"]
    question = quiz["question"]
    instructions = quiz["instructions"]
    resources = quiz.get("resources", [])

    data_summary = ""

    for res in resources:
        if res.lower().endswith(".pdf"):
            pdf_bytes = download_file(res)
            extracted = extract_pdf_tables(pdf_bytes)
            data_summary += f"\nPDF_FROM_{res}:\n{extracted}\n"
        else:
            try:
                data_summary += f"\nFILE({res}): Downloaded but not parsed.\n"
            except Exception:
                pass

    answer = await solve_task(question, instructions, data_summary)

    if answer is None:
        raise ValueError("LLM failed to compute final answer.")

    return submit_url, answer
