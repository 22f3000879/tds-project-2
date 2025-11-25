import json
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

async def extract_quiz_info(html: str):
    prompt = f"""
You are a quiz DOM parser. Extract the following fields strictly as JSON:

- question_text
- submit_url
- answer_instruction
- file_url (null if none)

Return ONLY valid JSON. No explanations.

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

    # --- CLEAN JSON ---
    cleaned = raw.strip()

    # Remove fenced code blocks
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1].strip()

    cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    # --- STRIP EVERYTHING BEFORE FIRST "{" ---
    idx = cleaned.find("{")
    if idx != -1:
        cleaned = cleaned[idx:]

    # Now cleaned is guaranteed to start with '{'
    try:
        data = json.loads(cleaned)
    except Exception as e:
        print("JSON PARSE ERROR:", e, cleaned)
        raise ValueError("LLM returned invalid JSON")

