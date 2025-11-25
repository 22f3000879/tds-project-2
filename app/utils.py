import re

def extract_between(text, start, end):
    s = text.find(start)
    if s == -1:
        return None
    s += len(start)
    e = text.find(end, s)
    if e == -1:
        return None
    return text[s:e].strip()

def clean_text(t: str):
    return re.sub(r"\s+", " ", t).strip()
