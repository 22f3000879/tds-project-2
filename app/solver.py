from .fetcher import fetch_page
from .llm import llm
from .parser import parse_quiz

async def solve_once(url: str):
    html = await fetch_page(url)
    question, submit_url = parse_quiz(html)

    prompt = f"""
    You will receive a quiz question or data task.
    Solve mathematically, precisely, and return only the final answer.

    QUESTION:
    {question}
    """

    answer = await llm(prompt)
    return submit_url, answer
