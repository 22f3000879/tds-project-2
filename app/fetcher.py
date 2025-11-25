import httpx
from bs4 import BeautifulSoup
import base64
import re

async def fetch_page(url: str) -> str:
    """Fetch webpage (no JS). Handle base64 DOM-injected HTML."""
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        r.raise_for_status()
        html = r.text

    # Detect base64 injected pages like sample Q834
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script")
    if script and "atob" in script.text:
        match = re.search(r"atob\(`([^`]+)`\)", script.text)
        if match:
            decoded = base64.b64decode(match.group(1)).decode()
            return decoded

    return html
