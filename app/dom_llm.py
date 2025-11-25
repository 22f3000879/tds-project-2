import openai
from app.config import OPENAI_API_KEY, OPENAI_MODEL

openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = """
You are a DOM extraction assistant.

Your job:
1. Read messy HTML / JavaScript.
2. Infer the quiz question.
3. Extract:
   - question_id
   - download_url (if PDF/CSV/API)
   - submit_url
   - task_description in plain English
Always output a JSON object only.
"""

async def llm_extract_dom(text: str) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        import json
        return json.loads(response.choices[0].message["content"])
    except Exception as e:
        print("LLM DOM extraction error:", e)
        return {}
