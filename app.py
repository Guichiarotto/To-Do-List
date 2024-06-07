import tkinter as tk
from tkinter import messagebox, simpledialog
from task import Task

class TimerWindow(tk.Toplevel):
    def __init__(self, parent, task):
        super().__init__(parent)
        self.parent = parent
        self.task = task
        self.title("Task Timer")

        self.config(bg="#ADD8E6")  # Background color

        self.time_label = tk.Label(self, text="00:00:00", font=("Arial", 24), bg="#ADD8E6")
        self.time_label.pack(padx=20, pady=20)

        self.button_frame = tk.Frame(self, bg="#ADD8E6")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_timer, bg="#90EE90")
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_timer, bg="#FF6347")
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.button_frame, text="Restart", command=self.restart_timer, bg="#FFD700")
        self.restart_button.pack(side=tk.LEFT, padx=10)

        self.update_time()

    def start_timer(self):
        self.task.start_task()
        self.update_time()

    def stop_timer(self):
        self.task.stop_task()

    def restart_timer(self):
        self.task.remaining_time = self.task.parse_time(self.task.estimated_time)
        self.update_time()

    def update_time(self):
        total_seconds = self.task.remaining_time
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_string)
        if self.task.start_time is not None:
            self.after(1000, self.update_time)


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("600x500")

        self.root.config(bg="#ADD8E6")  # Background color

        self.tasks = []

        self.frame = tk.Frame(root, bg="#ADD8E6")
        self.frame.pack(pady=10)

        self.listbox = tk.Listbox(self.frame, width=70, height=15, selectmode=tk.SINGLE, bg="#E6E6FA")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.entry = tk.Entry(root, width=70, bg="white")  # White background
        self.entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#90EE90")  # Green
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Edit Task", command=self.edit_task, bg="#FFD700")  # Yellow
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task, bg="#FF6347")  # Red
        self.delete_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Mark as Complete", command=self.complete_task, bg="#C0C0C0")  # Silver
        self.complete_button.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Task", command=self.start_task, bg="#90EE90")  # Green
        self.start_button.pack(pady=5)

        self.update_task_time()

    def add_task(self):
        description = self.entry.get()
        if description:
            due_time = simpledialog.askstring("Due Time", "Enter the due time (e.g., 14:00):")
            estimated_time = simpledialog.askstring("Estimated Time", "Enter the estimated time (HH:MM):")
            try:
                # Ensure the estimated_time is in the correct format
                hours, minutes = map(int, estimated_time.split(':'))
                if 0 <= hours < 24 and 0 <= minutes < 60:
                    task = Task(description, due_time, estimated_time)
                    self.tasks.append(task)
                    self.update_listbox()
                    self.entry.delete(0, tk.END)
                else:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Warning", "The estimated time must be in the format HH:MM.")
        else:
            messagebox.showwarning("Warning", "You must enter a task description.")

    def edit_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            new_description = simpledialog.askstring("Edit Task", "Edit the task description:", initialvalue=task.description)
            new_due_time = simpledialog.askstring("Edit Due Time", "Edit the due time:", initialvalue=task.due_time)
            new_estimated_time = simpledialog.askstring("Edit Estimated Time", "Edit the estimated time (HH:MM):", initialvalue=task.estimated_time)
            try:
                hours, minutes = map(int, new_estimated_time.split(':'))
                if new_description and new_due_time and 0 <= hours < 24 and 0 <= minutes < 60:
                    task.description = new_description
                    task.due_time = new_due_time
                    task.estimated_time = new_estimated_time
                    task.remaining_time = task.parse_time(new_estimated_time)
                    self.update_listbox()
                else:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Warning", "The estimated time must be in the format HH:MM.")
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to edit.")

    def delete_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            del self.tasks[selected_task_index]
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def complete_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            self.tasks[selected_task_index].mark_as_complete()
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to mark as complete.")

    def start_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            selected_task = self.tasks[selected_task_index]
            for task in self.tasks:
                task.stop_task()
            selected_task.start_task()
            self.update_listbox()
            self.open_timer_window(selected_task)
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to start.")

    def open_timer_window(self, task):
        timer_window = TimerWindow(self.root, task)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)

    def update_task_time(self):
        for task in self.tasks:
            task.update_remaining_time()
        self.root.after(1000, self.update_task_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
