import json, re, base64, traceback
import pandas as pd
import httpx
import io
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from .browser import fetch_page
from .llm_pipe import ask_llm
from .config import EMAIL, SECRET

SYSTEM_PROMPT = """
You are a data-analysis quiz solver.
Given the quiz text, files, and dataframe previews,
output ONLY this JSON:
{
 "answer": ...,
 "python": "...",
 "needs_plot": true/false
}
Python must define a variable 'result'.
If needs_plot, save plot to '/mnt/data/plot.png'.
"""

async def solve_once(url: str):
    html = await fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    # Detect submit URL
    m = re.search(r"https?://[^ ]+/submit[^ ]*", text)
    submit_url = m.group(0) if m else None

    # Download files
    files = [a["href"] for a in soup.find_all("a", href=True)]
    dfs = {}
    summaries = {}

    async with httpx.AsyncClient() as client:
        for f in files:
            try:
                r = await client.get(f)
                if f.endswith(".csv"):
                    df = pd.read_csv(io.StringIO(r.text))
                    dfs[f] = df
                    summaries[f] = df.head().to_string()

                elif f.endswith(".xlsx") or f.endswith(".xls"):
                    df = pd.read_excel(io.BytesIO(r.content))
                    dfs[f] = df
                    summaries[f] = df.head().to_string()

                elif f.endswith(".pdf"):
                    summaries[f] = f"PDF file size: {len(r.content)} bytes"

                else:
                    summaries[f] = f"Raw file ({len(r.content)} bytes)"

            except Exception as e:
                summaries[f] = f"Error processing file: {e}"

    user_prompt = f"""
Quiz text:
{text}

File summaries:
{json.dumps(summaries, indent=2)}

DataFrames:
{ {k: v.head().to_string() for k, v in dfs.items()} }

Follow output JSON format strictly.
"""

    llm_raw = await ask_llm(SYSTEM_PROMPT, user_prompt)

    try:
        parsed = json.loads(llm_raw)
    except:
        parsed = {"answer": llm_raw, "python": "", "needs_plot": False}

    answer = parsed["answer"]

    # Execute Python if provided
    if parsed.get("python"):
        try:
            local_env = {"dfs": dfs, "pd": pd, "plt": plt}
            exec(parsed["python"], {}, local_env)

            if "result" in local_env:
                answer = local_env["result"]

            if parsed.get("needs_plot"):
                plt.savefig("/mnt/data/plot.png")
                with open("/mnt/data/plot.png", "rb") as f:
                    ans = base64.b64encode(f.read()).decode()
                    answer = f"data:image/png;base64,{ans}"

        except Exception as e:
            answer = f"Python execution error: {e}"

    return submit_url, answer
