def build_prompt(html: str) -> str:
    return f"""
You are a STRICT JSON generator.

RULES:
- Output ONLY valid JSON.
- NO explanations.
- NO markdown.
- JSON structure MUST be a list of objects:
[
  {{"answer": "...", "submit_url": "..."}}
]

Extract all quiz questions from the HTML below, solve them, and return JSON only.

HTML:
{html}
"""
