import io
import pdfplumber
import httpx
import pandas as pd

async def solve_question(decoded_html: str, data: dict):
    file_url = data["url"]

    async with httpx.AsyncClient(timeout=30) as client:
        pdf_bytes = (await client.get(file_url)).content

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page2 = pdf.pages[1]
        table = page2.extract_table()

    df = pd.DataFrame(table[1:], columns=table[0])
    df["value"] = pd.to_numeric(df["value"])

    return df["value"].sum()
