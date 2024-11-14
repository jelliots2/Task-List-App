import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
import json

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.tasks = self.load_tasks()

        # Set up style
        self.setup_style()

        # Main entry for tasks
        self.task_input = ttk.Entry(self.root, width=50)
        self.task_input.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.task_input.bind("<Return>", lambda event: self.add_task())
        # Button to add tasks
        self.add_task_button = ttk.Button(self.root, text="Add Task", command=self.add_task, style="Custom.TButton")
        self.add_task_button.grid(row=0, column=1, padx=5, pady=5)

        # Listbox to display tasks
        self.tasks_listbox = tk.Listbox(self.root, width=50, bg="#f0f0f0", fg="black")
        self.tasks_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Configure the grid to be responsive
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.tasks_listbox.bind("<Delete>", lambda event: self.delete_task())
        # Button to delete tasks
        self.delete_task_button = ttk.Button(self.root, text="Delete Task", command=self.delete_task, style="Custom.TButton")
        self.delete_task_button.grid(row=2, column=0, padx=5, pady=5)

        self.theme_button = ttk.Button(self.root, text="Toggle Theme", command=self.toggle_theme, style="Custom.TButton")
        self.theme_button.grid(row=2, column=1, padx=5, pady=5)

        # Load initial tasks
        self.load_tasks_to_listbox()
        
        self.dark_theme = False

    def setup_style(self):
        """Sets up styles for ttk widgets, similar to CSS styling."""
        # No need to create a Style instance here; ttkbootstrap handles it automatically
        pass

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
            self.tasks_listbox.config(bg="#f0f0f0", fg="black")
            self.dark_theme = False
        else:
            self.root.config(bg="black")
            self.tasks_listbox.config(bg="grey", fg="white")
            self.dark_theme = True

if __name__ == "__main__":
    # Use ttkbootstrap's Window to initialize with a theme
    root = ttk.Window(themename="flatly")  # Corrected to use ttkbootstrap's Window
    app = TodoApp(root)
    root.mainloop()
