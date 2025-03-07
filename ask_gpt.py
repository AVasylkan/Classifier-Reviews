import os
import json
import prompt as p
from dotenv import load_dotenv

load_dotenv()

def ask_tema_restaurant(session, review_text, project):
    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv("API_KEY_AI")}"
        }

    if project == "fitness":
        data = {
            "messages": [
                {"role": "system", "content": p.PROMPT_TEMA_FITNESS},
                {"role": "user", "content": f"Вот отзыв: {review_text}"}
            ],
            "max_tokens": 500,
            "model": 'gpt-3.5-turbo',
        }

    else:
        data = {
            "messages": [
                {"role": "system", "content": p.PROMPT_TEMA_RESTAURANT},
                {"role": "user", "content": f"Вот отзыв: {review_text}"}
            ],
            "max_tokens": 500,
            "model": 'gpt-3.5-turbo',
        }

    response = session.post(os.getenv("ASK_URL"), headers=headers, data=json.dumps(data))
    response.raise_for_status()
    result = response.json()
    return result['choices'][0]['message']['content']