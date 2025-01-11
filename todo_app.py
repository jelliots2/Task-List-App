import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
#from tkinter import messagebox (If you want to use the optional message box. Uncomment if needed)
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        
        # Dictionary to store multiple task lists
        self.task_lists = self.load_task_lists()
        self.current_list = None
        
        # Frame for list selection
        self.list_frame = ttk.Frame(self.root)
        self.list_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Combobox for list selection
        self.list_selector = ttk.Combobox(self.list_frame, values=list(self.task_lists.keys()))
        self.list_selector.grid(row=0, column=0, padx=5, sticky="ew")
        self.list_selector.bind('<<ComboboxSelected>>', self.change_list)
        
        # Button to create new list
        self.new_list_button = ttk.Button(self.list_frame, text="New List", command=self.create_new_list)
        self.new_list_button.grid(row=0, column=1, padx=5)

        # Button to rename current list
        self.rename_list_button = ttk.Button(self.list_frame, text="Rename List", command=self.rename_list)
        self.rename_list_button.grid(row=0, column=2, padx=5)

        # Main entry for tasks
        self.task_input = ttk.Entry(self.root, width=50)
        self.task_input.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.task_input.bind("<Return>", lambda event: self.add_task())
        
        # Button to add tasks
        self.add_task_button = ttk.Button(self.root, text="Add Task", command=self.add_task, bootstyle="success")
        self.add_task_button.grid(row=1, column=1, padx=5, pady=5)

        # Frame for Listbox and Scrollbars (vertical and horizontal)
        listbox_frame = ttk.Frame(self.root)
        listbox_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

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
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Button to delete tasks
        self.delete_task_button = ttk.Button(self.root, text="Delete Task", command=self.delete_task, bootstyle="danger")
        self.delete_task_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Button to toggle theme
        self.theme_button = ttk.Button(self.root, text="Toggle Theme", command=self.toggle_theme, bootstyle="primary")
        self.theme_button.grid(row=3, column=1, padx=5, pady=5)

        # Button to delete current list
        self.delete_list_button = ttk.Button(self.root, text="Delete List", command=self.delete_list, bootstyle="danger")
        self.delete_list_button.grid(row=0, column=1, padx=5)

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

    def load_task_lists(self):
        try:
            with open('tasks.json', 'r') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {"Default": data}
        except (FileNotFoundError, json.JSONDecodeError):
            return {"Default": []}

    def save_task_lists(self):
        with open('tasks.json', 'w') as f:
            json.dump(self.task_lists, f)

    def create_new_list(self):
        dialog = ttk.Toplevel(self.root)
        dialog.title("New List")
        
        ttk.Label(dialog, text="Enter list name:").pack(pady=5)
        entry = ttk.Entry(dialog)
        entry.pack(pady=5)
        
        def save_list():
            name = entry.get().strip()
            if name and name not in self.task_lists:
                self.task_lists[name] = []
                self.list_selector['values'] = list(self.task_lists.keys())
                self.list_selector.set(name)
                self.current_list = name
                self.save_task_lists()
                self.load_tasks_to_listbox()
                dialog.destroy()
        
        ttk.Button(dialog, text="Create", command=save_list).pack(pady=5)

    def change_list(self, event=None):
        self.current_list = self.list_selector.get()
        self.load_tasks_to_listbox()

    def delete_list(self):
        if self.current_list and self.current_list != "Default":
            # Delete the current list
            del self.task_lists[self.current_list]
            
            # If no lists remain, create a Default list
            if not self.task_lists:
                self.task_lists["Default"] = []
            
            # Update combobox and select first available list
            self.list_selector['values'] = list(self.task_lists.keys())
            self.list_selector.set(list(self.task_lists.keys())[0])
            self.current_list = self.list_selector.get()
            
            self.save_task_lists()
            self.load_tasks_to_listbox()

    def load_tasks_to_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        if self.current_list:
            for task in self.task_lists[self.current_list]:
                task_with_bullet = f"• {task}"
                self.tasks_listbox.insert(tk.END, task_with_bullet)

    def add_task(self):
        task = self.task_input.get().strip()
        if task and self.current_list:
            self.task_lists[self.current_list].append(task)
            self.save_task_lists()
            self.load_tasks_to_listbox()
            self.task_input.delete(0, tk.END)

    def delete_task(self):
        if not self.current_list:
            return
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            selected_index = selected_task_index[0]
            del self.task_lists[self.current_list][selected_index]
            self.save_task_lists()
            self.load_tasks_to_listbox()

    def delete_task_on_key(self, event):
        """Deletes the selected task when the Delete key is pressed."""
        self.delete_task()

    def delete_list_on_key(self, event):
        self.delete_list()  

    def toggle_theme(self):
        if self.dark_theme:
            self.root.config(bg="white")
            self.tasks_listbox.config(bg="#f0f0f0", fg="black")
            self.dark_theme = False
        else:
            self.root.config(bg="black")
            self.tasks_listbox.config(bg="grey", fg="white")
            self.dark_theme = True

    def rename_list(self):
        if not self.current_list:
            return
            
        dialog = ttk.Toplevel(self.root)
        dialog.title("Rename List")
        
        ttk.Label(dialog, text="Enter new name:").pack(pady=5)
        entry = ttk.Entry(dialog)
        entry.insert(0, self.current_list)
        entry.pack(pady=5)
        
        def save_rename():
            new_name = entry.get().strip()
            if new_name and new_name != self.current_list and new_name not in self.task_lists:
                # Store tasks temporarily
                tasks = self.task_lists[self.current_list]
                # Delete old key
                del self.task_lists[self.current_list]
                # Add new key with same tasks
                self.task_lists[new_name] = tasks
                # Update combobox values
                self.list_selector['values'] = list(self.task_lists.keys())
                self.list_selector.set(new_name)
                self.current_list = new_name
                self.save_task_lists()
                dialog.destroy()
        
        ttk.Button(dialog, text="Rename", command=save_rename).pack(pady=5)

if __name__ == "__main__":
    # Use ttkbootstrap's Window to initialize with a theme
    root = ttk.Window(themename="flatly")
    app = TodoApp(root)
    root.mainloop()
