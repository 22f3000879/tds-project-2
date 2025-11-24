def build_prompt(html: str) -> str:
    return f"""
You are a strict JSON generator.

Extract exactly ONE question from this quiz HTML.
Find:
- the question text
- the options if any
- the correct answer using reasoning
- the submit URL (usually the form action)

RETURN JSON ONLY in this format:

[
  {{
    "answer": "...",
    "submit_url": "..."
  }}
]

Rules:
- DO NOT return explanations.
- DO NOT escape JSON.
- ALWAYS return a non-empty list.
- ALWAYS include submit_url.

HTML CONTENT BELOW:
----------------------------------------------------------------
{html}
----------------------------------------------------------------
"""
