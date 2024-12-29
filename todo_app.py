
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
#from tkinter import messagebox (If you want to use the optional message box. Uncomment if needed)
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.tasks = self.load_tasks()

        # Main entry for tasks
        self.task_input = ttk.Entry(self.root, width=50)
        self.task_input.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.task_input.bind("<Return>", lambda event: self.add_task())
        
        # Button to add tasks
        self.add_task_button = ttk.Button(self.root, text="Add Task", command=self.add_task, bootstyle="success")
        self.add_task_button.grid(row=0, column=1, padx=5, pady=5)

        # Frame for Listbox and Scrollbars (vertical and horizontal)
        listbox_frame = ttk.Frame(self.root)
        listbox_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Configure the grid to be responsive
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)

        # Listbox to display tasks
        self.tasks_listbox = tk.Listbox(listbox_frame, height=10, width=50, bg="#f0f0f0", fg="black", font=("Helvetica", 16), selectmode=tk.SINGLE)
        self.tasks_listbox.grid(row=0, column=0, sticky="nsew")

        # Vertical scrollbar for the Listbox
        self.v_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.tasks_listbox.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.tasks_listbox.config(yscrollcommand=self.v_scrollbar.set)

        # Horizontal scrollbar for the Listbox
        self.h_scrollbar = ttk.Scrollbar(listbox_frame, orient="horizontal", command=self.tasks_listbox.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.tasks_listbox.config(xscrollcommand=self.h_scrollbar.set)

        # Configure the grid to be responsive
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Button to delete tasks
        self.delete_task_button = ttk.Button(self.root, text="Delete Task", command=self.delete_task, bootstyle="danger")
        self.delete_task_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Button to toggle theme
        self.theme_button = ttk.Button(self.root, text="Toggle Theme", command=self.toggle_theme, bootstyle="primary")
        self.theme_button.grid(row=2, column=1, padx=5, pady=5)

        # Load initial tasks
        self.load_tasks_to_listbox()
        self.dark_theme = False
        
        # Set up style
        self.setup_style()
        
        self.tasks_listbox.bind("<Delete>", self.delete_task_on_key)

    def setup_style(self):
        """Sets up styles for ttk widgets, similar to CSS styling."""
        style = ttk.Style()

        # Define a custom button style with larger text
        style.configure("Custom.TButton", font=("Helvetica", 16))

        # Define a custom entry style with larger text
        style.configure("Custom.TEntry", font=("Helvetica", 16))

        # Larger font for the Listbox
        self.tasks_listbox.config(font=("Helvetica", 16))

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
            task_with_bullet = f"• {task}"
            self.tasks_listbox.insert(tk.END, task_with_bullet)

    def add_task(self):
        task = self.task_input.get()
        if task:
            self.tasks.append(task)
            self.save_tasks()
            self.load_tasks_to_listbox()
            self.task_input.delete(0, tk.END)
        # else: Optional message box. Stupid because self explanatory. (uncomment if needed)
            #messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):
        selected_task_index = self.tasks_listbox.curselection()  # Get the selected task
        if selected_task_index:  # Check if a task is selected
            selected_index = selected_task_index[0]  # Extract the index
            task = self.tasks[selected_index]
            # Remove the task from the tasks list
            del self.tasks[selected_index]
            # Remove the task from the Listbox
            self.tasks_listbox.delete(selected_index)
            # Save the updated tasks list to the file
            self.save_tasks()
        # Optional message box. Stupid because self explanatory... Again... (Uncomment if needed)
        #else:
            #messagebox.showwarning("Warning", "Please select a task to delete.")

    def delete_task_on_key(self, event):
        """Deletes the selected task when the Delete key is pressed."""
        self.delete_task()

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
    root = ttk.Window(themename="flatly")
    app = TodoApp(root)
    root.mainloop()
