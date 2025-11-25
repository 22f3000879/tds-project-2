import openai
from app.config import OPENAI_API_KEY, OPENAI_MODEL

openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = """
You are a quiz-solving assistant.
You NEVER hallucinate numbers.
You only compute using provided data.

If unsure, say "PARSE_ERROR".
Return ONLY JSON:
{
  "answer": ...
}
"""

async def llm_answer(question_text: str, data_text: str) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"QUESTION:\n{question_text}\n\nDATA:\n{data_text}"}
            ],
            temperature=0
        )
        import json
        return json.loads(response.choices[0].message["content"])
    except Exception as e:
        print("LLM Answer error:", e)
        return {"answer": None}
