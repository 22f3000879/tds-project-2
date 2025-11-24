from bs4 import BeautifulSoup

def parse_quiz(html: str):
    soup = BeautifulSoup(html, "html.parser")

    question = soup.get_text(separator="\n")
    submit_url = None

    for script in soup.find_all("script"):
        if "submit" in script.text:
            if "https://" in script.text:
                part = script.text.split("https://", 1)[1]
                submit_url = "https://" + part.split('"')[0]

    return question, submit_url
