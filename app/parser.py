from bs4 import BeautifulSoup
import re
import json

def parse_quiz(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # Find instructions in text
    text = soup.get_text(" ", strip=True)

    # Extract submit URL (visible in example)
    submit = None
    for a in soup.find_all("a", href=True):
        if "submit" in a["href"]:
            submit = a["href"]
            break

    # Extract file link if present
    file_url = None
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith((".pdf", ".csv", ".xlsx")):
            file_url = href
            break

    return {
        "instructions": text,
        "file_url": file_url,
        "submit_url": submit
    }
