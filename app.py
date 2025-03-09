from flask import request, jsonify
from requests import Session
from functions import (
    get_review_text,
    crm_update_tema,
    ask_tema, format_ask,
    is_valid,
    app)



@app.route('/')
def tema():

    with Session() as session:

        id_item = int(request.args.get('id_item'))
        project = str(request.args.get('project'))  #restaurant or fitness

        review_text = get_review_text(session, id_item, project)
        if not review_text:
            return jsonify({'result': 'Отзыв не найден'})
        
        ask_gpt = ask_tema(session, review_text, project)
        if not review_text:
            return jsonify({'result': 'Отзыв не класифицирован'})

        if project == 'restaurant':
            formats = is_valid(ask_gpt)
            if not formats:
                ask_gpt = format_ask(ask_gpt)
                if not ask_gpt:
                    return jsonify({'result': 'Значение класификации не отформатировано'})

            result = crm_update_tema(session, id_item, ask_gpt, project)
            if not result:
                return jsonify({'result': 'Отзыв не обновлен в CRM'})

        elif project == 'fitness':
            result = crm_update_tema(session, id_item, ask_gpt, project)
            if not result:
                return jsonify({'result': 'Отзыв не обновлен в CRM'})
            
        return jsonify({'result': ask_gpt})


if __name__ == '__main__':
    app.run(debug=True)

#http://127.0.0.1:5000?id_item=104308&project=restaurant
#http://127.0.0.1:5000?id_item=12154&project=fitness

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000)

# pip freeze > requirements.txt