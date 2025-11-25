from .fetcher import fetch_page
from .dom_llm import render_dom
from .quiz_llm import interpret_quiz
from .submit import submit_answer
from .utils import download_file, extract_pdf_table_sum
from .config import EMAIL, SECRET
import time

async def solve_once(initial_url: str):

    url = initial_url
    start_time = time.time()

    while True:

        raw_html = await fetch_page(url)
        final_html = await render_dom(raw_html)
        interpretation = await interpret_quiz(final_html)

        submit_url = interpretation["submit_url"]
        download_url = interpretation["download_url"]
        needs_compute = interpretation["needs_compute"]
        expected_action = interpretation["expected_action"]

        answer = interpretation["answer"]

        if needs_compute:
            if expected_action == "pdf_sum":
                file_bytes = await download_file(download_url)
                answer = extract_pdf_table_sum(file_bytes)

        payload = {
            "email": EMAIL,
            "secret": SECRET,
            "url": url,
            "answer": answer
        }

        result = await submit_answer(submit_url, payload)

        if "url" not in result or not result["url"]:
            return result

        url = result["url"]

        if time.time() - start_time > 170:
            return {"correct": False, "reason": "Timeout 3 minutes"}

