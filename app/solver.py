from .browser import fetch_page
from .llm import ask_llm
import re

async def solve_once(url: str):
    html = await fetch_page(url)

    # Extract submit URL from HTML
    m = re.search(r'"submit"\s*:\s*"([^"]+)"', html)
    submit_url = m.group(1) if m else None

    # Let LLM analyze question + HTML
    prompt = f"""
You will receive HTML of a quiz page.
Extract the correct answer ONLY.

HTML:
{html}

Answer format: return only the raw value (number/string/boolean).
"""

    answer = await ask_llm(prompt)

    return submit_url, answer.strip()
