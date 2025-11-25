import base64
import httpx
import pandas as pd
from PyPDF2 import PdfReader
from io import BytesIO

async def download_file(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.content

def extract_pdf_table_sum(pdf_bytes: bytes, column_name="value", page=1):
    reader = PdfReader(BytesIO(pdf_bytes))
    text = reader.pages[page].extract_text()

    rows = []
    for line in text.split("\n"):
        parts = line.split()
        if len(parts) >= 2:
            try:
                num = float(parts[-1])
                rows.append(num)
            except:
                pass

    return sum(rows)
