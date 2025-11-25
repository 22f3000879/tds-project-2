import os

SECRET = os.getenv("TDS_SECRET", "")
EMAIL = os.getenv("TDS_EMAIL", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4.1-mini"   # Good balance between speed + cost
