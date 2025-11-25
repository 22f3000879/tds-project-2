import json
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

async def solve_task(question: str, instructions: str, data_summary: str):
    """
    LLM computes final answer from extracted data.
    """

    system_prompt = """
You are an advanced quiz solver.
You ALWAYS return valid JSON only.

Format:
{"answer": ...}
    """

    user_prompt = f"""
QUESTION:
{question}

INSTRUCTIONS:
{instructions}

DATA SUMMARY:
{data_summary}

Return JSON only.
"""

    r = client.responses.create(
        model=OPENAI_MODEL,
        input=[{"role": "system", "content": system_prompt},
               {"role": "user", "content": user_prompt}],
        max_output_tokens=300,
        temperature=0
    )

    try:
        return json.loads(r.output_text)["answer"]
    except Exception:
        print("LLM Quiz compute error:", r.output_text)
        return None
