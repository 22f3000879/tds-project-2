import json
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

async def extract_quiz_info(html: str):
    prompt = f"""
You are a quiz solver. Extract the following strictly as JSON:

- question_text
- submit_url
- answer_instruction (what the quiz wants)
- file_url (if any file needs downloading)

HTML:
{html}

Return JSON only.
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        temperature=0
    )

    raw = response.output_text
    print("LLM RAW:", raw)
    return raw
