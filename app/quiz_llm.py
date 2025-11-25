from openai import OpenAI
from .config import AIPIPE_TOKEN, OPENAI_BASE_URL, MODEL

client = OpenAI(api_key=AIPIPE_TOKEN, base_url=OPENAI_BASE_URL)

async def interpret_quiz(final_html: str) -> dict:
    system_prompt = """
You are an expert data analysis quiz solver.

Given FINAL rendered HTML:
- extract submit_url
- extract question description
- extract any file download links
- decide what data processing is required
- describe steps
- predict answer (if answer requires computation you must explain)

Return ONLY valid JSON:
{
 "submit_url": "...",
 "download_url": "... or null",
 "answer_type": "...",
 "steps": "...",
 "needs_compute": true/false,
 "expected_action": "pdf_sum/table/api/chart/etc",
 "answer": null  // if computation needed
}
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_html}
        ]
    )

    import json
    return json.loads(resp.choices[0].message["content"])
