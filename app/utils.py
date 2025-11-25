import pandas as pd
import requests
from pypdf import PdfReader
from io import BytesIO

def download_file(url: str):
    r = requests.get(url)
    r.raise_for_status()
    return r.content


def extract_pdf_tables(pdf_bytes):
    reader = PdfReader(BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
