from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL
import json

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You solve quiz questions using ONLY the given data.
Never hallucinate numbers.
Return JSON only: { "answer": ... }
"""

async def llm_answer(question_text: str, data_text: str) -> dict:
    try:
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"QUESTION:\n{question_text}\n\nDATA:\n{data_text}"}
            ],
            temperature=0
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print("LLM Answer error:", e)
        return {"answer": None}
