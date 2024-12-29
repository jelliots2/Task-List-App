from flask import Flask, request, jsonify
from todo_app import TodoApp

app = Flask(__name__)
todo_app = TodoApp()  # Initialize with the refactored class

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(todo_app.get_tasks())

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = data.get('task')
    if task:
        todo_app.add_task(task)
        return jsonify({'message': 'Task added', 'task': task}), 201
    return jsonify({'error': 'Task is required'}), 400

@app.route('/tasks/<int:task_index>', methods=['DELETE'])
def delete_task(task_index):
    task = todo_app.delete_task(task_index)
    if task:
        return jsonify({'message': 'Task deleted', 'task': task}), 200
    return jsonify({'error': 'Invalid task index'}), 404

if __name__ == '__main__':
    app.run(debug=True)
