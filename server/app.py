import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS


TODOS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Купить хлеб',
        'desc': 'На рынке',
        'done': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Забрать котёнка',
        'desc': 'Левченко 56',
        'done': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Покормить рыбу',
        'desc': 'в 2 часа',
        'done': True
    }
]


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_todo(todo_id):
    for todo in TODOS:
        if todo['id'] == todo_id:
            TODOS.remove(todo)
            return True
    return False


@app.route('/todos', methods=['GET', 'POST'])
def all_todos():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TODOS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'desc': post_data.get('desc'),
            'done': post_data.get('done')
        })
        response_object['message'] = 'ToDo added!'
    else:
        response_object['todos'] = TODOS
    return jsonify(response_object)


@app.route('/todos/<todo_id>', methods=['PUT', 'DELETE'])
def single_todo(todo_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_todo(todo_id)
        TODOS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'desc': post_data.get('desc'),
            'done': post_data.get('done')
        })
        response_object['message'] = 'ToDo updated!'
    if request.method == 'DELETE':
        remove_todo(todo_id)
        response_object['message'] = 'ToDo removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
