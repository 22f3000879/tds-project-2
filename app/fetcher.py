import httpx
from bs4 import BeautifulSoup

async def fetch_page(url: str) -> str:
    """
    Fetches HTML content. JS-rendered? Server already serves rendered DOM.
    """
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text


def clean_html(raw_html: str) -> str:
    """
    Remove scripts, styles, unnecessary tags.
    """
    soup = BeautifulSoup(raw_html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text("\n")
