import os
import prompt
import json
from logging import FileHandler
from flask import Flask
from flask.logging import create_logger
from dotenv import load_dotenv


app = Flask(__name__)

logger = create_logger(app)
logger.addHandler(FileHandler('log_file.log'))

load_dotenv()


def get_review_text(session, id_item, project):

    url = os.getenv("GET_URL")
    headers = {
        "Content-Type": "application/json",
        'scope': 'crm'
    }

    try:
        if project == "fitness":
            params = dict(entityTypeId=177, id=id_item)
            response = session.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data['result']['item']['ufCrm12_1649502676']

        elif project == "restaurant":
            params = dict(entityTypeId=178, id=id_item)
            response = session.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data['result']['item']['ufCrm5_1644313449']
        
        
    except Exception as e:
        logger.error(e, exc_info=True)
        return False
    


def ask_tema(session, review_text, project):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv("API_KEY_AI")}"
    }

    try:
        if project == "fitness":
            data = {
                "messages": [
                    {"role": "system", "content": prompt.PROMPT_TEMA_FITNESS},
                    {"role": "user", "content": f"Вот отзыв: {review_text}"}
                ],
                "max_tokens": 1000,
                "model": 'gpt-3.5-turbo',
            }

        elif project == "restaurant":
            data = {
                "messages": [
                    {"role": "system", "content": prompt.PROMPT_TEMA_RESTAURANT},
                    {"role": "user", "content": f"Вот отзыв: {review_text}"}
                ],
                "max_tokens": 1000,
                "model": 'gpt-3.5-turbo',
            }

        response = session.post(os.getenv("ASK_URL"), headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        logger.error(e, exc_info=True)
        return False



def is_valid(value):
    if isinstance(value, (int, float)) and str(value).isdigit():
        return True
    return False



def format_ask(value):
    if isinstance(value, str):
        parts = value.split(',')
        cleaned_parts = ["".join(filter(lambda x: x.isdigit(), part)) for part in parts]
        cleaned_parts = [part for part in cleaned_parts if part]

        if len(cleaned_parts) == 1:
            return int(cleaned_parts[0])

        elif len(cleaned_parts) == 2:
            return f"{int(cleaned_parts[0])},{int(cleaned_parts[1])}"

    return value if isinstance(value, int) else False



def crm_update_tema(session, id_item, ask_gpt, project):

    try:
        if project == "fitness":
            param = dict(entityTypeId=177, id=id_item, fields={
                "ufCrm12_1649502657": ask_gpt
            }, scope='crm')

        elif project == "restaurant":
            param = dict(entityTypeId=178, id=id_item, fields={
                "ufCrm5_1692100077": [ask_gpt]
            }, scope='crm')

        resp = session.post(os.getenv("UPDATE_URL"), json=param)
        response_json = resp.json()
        return response_json

    except Exception as e:
        logger.error(e, exc_info=True)
        return False







