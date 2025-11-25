from openai import OpenAI
from .config import AIPIPE_TOKEN, OPENAI_BASE_URL, MODEL

client = OpenAI(api_key=AIPIPE_TOKEN, base_url=OPENAI_BASE_URL)

async def render_dom(raw_html: str) -> str:
    system_prompt = """
You are a browser engine.
Simulate DOM execution:
- Execute <script> tags mentally
- Support atob(), innerHTML, DOM writes
- Compute final rendered HTML

Return ONLY the final HTML. No explanation.
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_html}
        ]
    )

    return resp.choices[0].message["content"]
