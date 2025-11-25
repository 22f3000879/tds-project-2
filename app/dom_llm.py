import json
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

async def extract_quiz_info(html_text: str):
    """
    Use LLM to extract:
        - question type
        - what to compute
        - download URLs
        - submit URL
    Must return valid JSON always.
    """

    system_prompt = """
You are a DOM analysis assistant.
Your job is to read the extracted text of a quiz page and return structured JSON.

Output format:
{
  "question": "...",
  "task_type": "...",
  "submit_url": "...",
  "resources": ["url1", "url2"],
  "instructions": "plain english description of what to compute"
}

If anything is missing, infer sensibly.
"""

    user_prompt = f"""
Extract quiz information from the page text:

PAGE_CONTENT:
{html_text}

Return ONLY valid JSON.
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[{"role": "system", "content": system_prompt},
               {"role": "user", "content": user_prompt}],
        reasoning={"effort": "medium"},
        max_output_tokens=400,
        temperature=0
    )

    try:
        content = response.output_text
        data = json.loads(content)
        return data
    except Exception:
        print("LLM DOM extraction error:", content)
        return None
