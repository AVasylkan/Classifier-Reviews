import os
from dotenv import load_dotenv

load_dotenv()


def get_review_text(session, id_item, project):
    url = os.getenv("GET_URL")
    headers = {
        "Content-Type": "application/json",
        'scope': 'crm'
    }

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



def crm_update_tema(session, id_item, ask_gpt, project):
    if project == "fitness":
        param = dict(entityTypeId=177, id=id_item, fields={
            "ufCrm12_1649502657": ask_gpt
        }, scope='crm')

    else:
        param = dict(entityTypeId=178, id=id_item, fields={
            "ufCrm5_1692100077": [ask_gpt]
        }, scope='crm')

    resp = session.post(os.getenv("UPDATE_URL"), json=param)
    response_json = resp.json()
    return response_json