# main.py

import tkinter as tk
from app import ToDoApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
