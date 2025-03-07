from flask import request, jsonify, Flask
from requests import Session
from b24 import get_review_text, crm_update_tema
from ask_gpt import ask_tema_restaurant
from utils import format_ask, is_valid, handle_exception, app


@app.errorhandler(Exception)
def decorator_handle_exception(Exception):
    errors_exp = handle_exception(Exception)
    jsonify({'result': errors_exp})


@app.route('/')
def tema():
    with Session() as session:
        id_item = int(request.args.get('id_item'))
        project = str(request.args.get('project'))  #restaurant or fitness
        review_text = get_review_text(session, id_item, project)
        ask_gpt = ask_tema_restaurant(session, review_text, project)

        if project == 'restaurant':
            formats = is_valid(ask_gpt)

            if not formats:
                ask_gpt = format_ask(ask_gpt)
            crm_update_tema(session, id_item, ask_gpt, project)

        elif project == 'fitness':
            crm_update_tema(session, id_item, ask_gpt, project)

        return jsonify({'result': ask_gpt})


if __name__ == '__main__':
    app.run(debug=True)

#http://127.0.0.1:5000?id_item=104308&project=restaurant
#http://127.0.0.1:5000?id_item=104308&project=fitness
