def build_prompt(html: str) -> str:
    return f"""
You MUST return ONLY valid JSON. NO text before or after it.

Format exactly like:
[
  {{"answer": "...", "submit_url": "..."}}
]

Rules:
- Output ONLY JSON.
- No markdown.
- No explanations.

HTML to parse:
{html}
"""
