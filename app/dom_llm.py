from openai import AsyncOpenAI
import json
from app.config import OPENAI_API_KEY, OPENAI_MODEL

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a DOM extraction assistant.

Your job:
1. Read messy HTML / JavaScript.
2. Infer the quiz question.
3. Extract:
   - question_id
   - download_url
   - submit_url
   - task_description
Output strictly JSON only.
"""

async def llm_extract_dom(text: str) -> dict:
    try:
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print("LLM DOM extraction error:", e)
        return {}
