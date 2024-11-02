import tkinter as tk
from tkinter import messagebox
import json

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.tasks = self.load_tasks()

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=1)  # First row will expand
        self.root.grid_columnconfigure(0, weight=1)  # First column will expand

        self.task_input = tk.Entry(self.root, width=50)
        self.task_input.grid(row=0, column=0, padx=5, pady=5, sticky="ew")  # Expand horizontally

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=0, column=1, padx=5, pady=5)  # No expand

        self.tasks_listbox = tk.Listbox(self.root, width=50)
        self.tasks_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")  # Expand both horizontally and vertically

        self.load_tasks_to_listbox()

        self.delete_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.grid(row=2, column=0, padx=5, pady=5)  # No expand

        # Configure the grid to expand the listbox
        self.root.grid_rowconfigure(1, weight=1)  # Make the listbox row expandable

        self.theme_button = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.grid(row=2, column=1, padx=5, pady=5)  # No expand

        self.dark_theme = False

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)

    def load_tasks_to_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, task)

    def add_task(self):
        task = self.task_input.get()
        if task:
            self.tasks.append(task)
            self.save_tasks()
            self.load_tasks_to_listbox()
            self.task_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            self.save_tasks()
            self.load_tasks_to_listbox()

    def toggle_theme(self):
        if self.dark_theme:
            self.root.config(bg="white")
            self.tasks_listbox.config(bg="lightgrey", fg="black")
            self.add_task_button.config(bg="blue", fg="white")
            self.delete_task_button.config(bg="red", fg="black")
            self.dark_theme = False
        else:
            self.root.config(bg="black")
            self.tasks_listbox.config(bg="grey", fg="white")
            self.add_task_button.config(bg="green", fg="black")
            self.delete_task_button.config(bg="red", fg="white")
            self.dark_theme = True

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
