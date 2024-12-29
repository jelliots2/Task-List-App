import json

class TodoApp:
    def __init__(self, tasks_file='tasks.json'):
        self.tasks_file = tasks_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f)

    def get_tasks(self):
        return self.tasks

    def add_task(self, task):
        if task:
            self.tasks.append(task)
            self.save_tasks()
            return task

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            task = self.tasks.pop(task_index)
            self.save_tasks()
            return task
        return None
