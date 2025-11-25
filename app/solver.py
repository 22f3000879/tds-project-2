import base64
import httpx
from pypdf import PdfReader

from app.fetcher import fetch_html, extract_dom_text
from app.dom_llm import llm_extract_dom
from app.quiz_llm import llm_answer

async def solve_once(url: str, email: str, secret: str):
    html = await fetch_html(url)
    dom_text = await extract_dom_text(html)

    info = await llm_extract_dom(dom_text)

    submit_url = info.get("submit_url")
    download_url = info.get("download_url")
    question_text = info.get("task_description")

    if not submit_url:
        raise ValueError("LLM failed to identify submit_url")

    data_text = ""

    if download_url:
        # download PDF or other file
        r = await httpx.AsyncClient(timeout=20).get(download_url)
        content = r.content

        # If PDF
        if download_url.lower().endswith(".pdf"):
            reader = PdfReader(io.BytesIO(content))
            all_text = []
            for page in reader.pages:
                all_text.append(page.extract_text())
            data_text = "\n".join(all_text)
        else:
            # assume text/CSV
            try:
                data_text = content.decode("utf-8", errors="ignore")
            except:
                data_text = base64.b64encode(content).decode()

    # Use LLM to compute answer
    result = await llm_answer(question_text, data_text)
    answer = result.get("answer")

    if answer is None:
        raise ValueError("LLM failed to compute answer")

    return submit_url, answer
