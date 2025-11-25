import re
import base64
import json
from bs4 import BeautifulSoup

def extract_payload(html: str):
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", text=re.compile("atob"))
    if not script:
        raise ValueError("No <script> with base64 found.")

    # extract inside atob(`...`)
    match = re.search(r"atob\(`([^`]+)`\)", script.text)
    if not match:
        raise ValueError("Could not extract base64 string.")

    b64 = match.group(1)
    decoded = base64.b64decode(b64).decode("utf-8")

    # the decoded content contains HTML with <pre> containing JSON
    inner_soup = BeautifulSoup(decoded, "html.parser")
    pre = inner_soup.find("pre")

    if not pre:
        raise ValueError("No <pre> in decoded content.")

    data = json.loads(pre.text)

    # Example fields:
    # {
    #   "email": "...",
    #   "secret": "...",
    #   "url": "...",
    #   "answer": 12345
    # }

    return decoded, data
