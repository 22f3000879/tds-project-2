def build_prompt(html: str) -> str:
    return f"""
You are a quiz solver. Extract all questions from the HTML below and compute the correct answers.

Return result as JSON:
[
  {{"answer": "...", "submit_url": "URL to send answer"}}
]

HTML:
{html}
"""
