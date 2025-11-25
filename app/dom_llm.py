import json
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a QUIZ HTML PARSER.

Your ONLY job: extract structured JSON from quiz pages.
You MUST follow these strict rules:

1. NEVER invent instructions like “POST this JSON to /submit”.
2. NEVER guess missing values — use null instead.
3. NEVER output code fences (no ```).
4. ALWAYS output ONLY pure JSON.
5. ALWAYS return this exact structure:

{
  "question_text": "...",
  "submit_url": "... or null",
  "answer_instruction": "... or null",
  "file_url": "... or null"
}

Definitions:
- question_text: The actual question EXACTLY as shown in the HTML.
- submit_url: <form action="..."> or any submission endpoint found in the HTML.
- answer_instruction: Only if the HTML explicitly tells the user how to answer.
- file_url: Any PDF/CSV/image link needed to solve the quiz.

If something is not present IN THE HTML, return null for that field.

Do NOT add comments, explanations, descriptions, or text outside JSON.
"""


async def extract_quiz_info(html: str):
    prompt = f"{SYSTEM_PROMPT}\n\nHTML:\n{html}"

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        temperature=0,
    )

    raw = response.output_text
    print("LLM RAW:", raw)

    # ------------------------
    # CLEAN JSON OUTPUT
    # ------------------------
    cleaned = raw.strip()

    # remove code fences if any
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1].strip()

    cleaned = (
        cleaned.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # Ensure starts at '{'
    idx = cleaned.find("{")
    if idx != -1:
        cleaned = cleaned[idx:]

    # Final parse
    try:
        data = json.loads(cleaned)
        return data
    except Exception as e:
        print("\nJSON PARSE ERROR:", e, "\nCLEANED:\n", cleaned)
        raise ValueError("LLM returned invalid JSON")
