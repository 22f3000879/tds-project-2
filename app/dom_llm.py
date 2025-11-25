import json
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

async def extract_quiz_info(html: str):
    prompt = f"""
You are a strict JSON parser for quiz webpages.

Extract the following fields:

- question  : the quiz question text
- submit_url: the URL where answers must be POSTed
- instruction: any instruction about how to answer
- file_url  : link to any attached file (or null)

RETURN ONLY JSON. DO NOT ADD ``` BLOCKS.
DO NOT ADD EXTRA TEXT.

HTML:
{html}
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        temperature=0
    )

    raw = response.output_text
    print("LLM RAW:", raw)

    cleaned = raw.strip()

    # Remove fenced code blocks just in case
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    # Strip everything before first "{"
    idx = cleaned.find("{")
    if idx != -1:
        cleaned = cleaned[idx:]

    try:
        data = json.loads(cleaned)
    except Exception as e:
        print("JSON PARSE ERROR:", e, cleaned)
        raise ValueError("LLM returned invalid JSON")

    # Validate required keys
    for key in ["question", "submit_url", "instruction", "file_url"]:
        if key not in data:
            raise ValueError(f"LLM missing required field: {key}")

    return data
