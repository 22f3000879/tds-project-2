import httpx
from bs4 import BeautifulSoup

async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient(timeout=40) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text

async def fetch_file(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.content
