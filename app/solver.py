import json, re, base64, pandas as pd, httpx, traceback
from bs4 import BeautifulSoup
from .browser import fetch_page
from .llm_pipe import ask_llm
from .config import EMAIL, SECRET
import matplotlib.pyplot as plt
import io

SYSTEM_PROMPT = """
You are a quiz-solving data agent.
Input: page text, file contents, dataframe previews.
Output must be JSON only:
{
 "answer": ...,
 "python": "...",
 "needs_plot": true/false
}
Python must define a variable 'result'.
If needs_plot=true, save plot to '/mnt/data/plot.png'.
"""

async def solve_once(url: str):
    html = await fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    # Extract submit URL
    m = re.search(r"https?://[^ ]+/submit[^ ]*", page_text)
    submit_url = m.group(0) if m else None

    # File extraction
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
                elif f.endswith(".xlsx"):
                    df = pd.read_excel(io.BytesIO(r.content))
                    dfs[f] = df
                    summaries[f] = df.head().to_string()
                elif f.endswith(".pdf"):
                    summaries[f] = f"PDF file with {len(r.content)} bytes."
                else:
                    summaries[f] = f"File ({len(r.content)} bytes)."
            except Exception as e:
                summaries[f] = f"Error: {e}"

    user_prompt = f"""
Quiz text:
{page_text}

File summaries:
{json.dumps(summaries, indent=2)}

DataFrames:
{ {k:v.head().to_string() for k,v in dfs.items()} }

Produce JSON answer as instructed.
"""

    llm_raw = await ask_llm(SYSTEM_PROMPT, user_prompt)

    try:
        parsed = json.loads(llm_raw)
    except:
        parsed = {"answer": llm_raw, "python": "", "needs_plot": False}

    answer = parsed["answer"]

    # Execute python if provided
    if parsed.get("python"):
        try:
            local_env = {"dfs": dfs, "pd": pd, "plt": plt}
            exec(parsed["python"], {}, local_env)
            if "result" in local_env:
                answer = local_env["result"]

            if parsed.get("needs_plot"):
                plt.savefig("/mnt/data/plot.png")
                with open("/mnt/data/plot.png", "rb") as f:
                    img = base64.b64encode(f.read()).decode()
                    answer = "data:image/png;base64," + img

        except Exception as e:
            answer = f"Python execution error: {e}"

    return submit_url, answer
