import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader

def extract_answer(instructions: str, file_bytes: bytes = None):
    """
    Automatically interpret instructions.
    Uses rules + LLM in solver.py.
    """

    if not file_bytes:
        return None

    # PDF Example
    if "page 2" in instructions.lower() and "value" in instructions.lower():
        reader = PdfReader(BytesIO(file_bytes))
        # Extract text from page 2 (index 1)
        page = reader.pages[1]
        text = page.extract_text()

        # Convert detected table into dataframe
        import re
        rows = [line.split() for line in text.split("\n")]
        values = []
        for row in rows:
            for token in row:
                if token.isdigit():
                    values.append(int(token))

        return sum(values)

    return None
