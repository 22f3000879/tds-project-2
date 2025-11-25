import httpx
from bs4 import BeautifulSoup

client = httpx.AsyncClient(timeout=20)

async def fetch_html(url: str) -> str:
    r = await client.get(url)
    r.raise_for_status()
    return r.text

async def extract_dom_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Full rendered DOM may contain JS-generated content inside <script> as base64.
    # Extract visible + script base64-embedded content.
    text_parts = []

    for tag in soup.find_all():
        if tag.name == "script" and tag.string:
            text_parts.append(tag.string)
        if tag.text:
            text_parts.append(tag.text)

    return "\n".join(text_parts)
