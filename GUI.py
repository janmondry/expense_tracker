import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo


class GUI:
    def __init__(self, controller):
        self.controller = controller
        self.window = None

    def printGUI(self):
        self.window = tk.Tk()
        self.window.geometry("1024x800")
        self.window.title("ExpenseTracker")
        self.window.resizable(False, False)

    def destroyGUI(self):
        if self.window is not None:
            self.window.destroy()

