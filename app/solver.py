import re, json, base64, httpx, pandas as pd
from bs4 import BeautifulSoup
from .browser import load_page
from .config import EMAIL, SECRET

async def solve_quiz(url: str):
    html = await load_page(url)
    soup = BeautifulSoup(html, "html.parser")

    # Extract instructions
    text = soup.get_text(" ", strip=True)

    # Extract submit URL from page
    match = re.search(r"https?://\S+/submit\S*", text)
    submit_url = match.group(0) if match else None

    # Handle files if referenced
    file_links = [a["href"] for a in soup.find_all("a", href=True) if "pdf" in a["href"] or "csv" in a["href"]]

    dataframes = []
    for link in file_links:
        async with httpx.AsyncClient() as client:
            resp = await client.get(link)
        if "csv" in link:
            df = pd.read_csv(pd.compat.StringIO(resp.text))
            dataframes.append(df)

    # VERY SIMPLE AUTO SOLVER EXAMPLE
    answer = None

    if "sum" in text.lower() and "value" in text.lower():
        for df in dataframes:
            if "value" in df.columns:
                answer = float(df["value"].sum())

    # Default fallback
    if answer is None:
        answer = "Unable to intelligently infer answer."

    payload = {
        "email": EMAIL,
        "secret": SECRET,
        "url": url,
        "answer": answer
    }

    return submit_url, payload
