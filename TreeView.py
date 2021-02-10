import tkinter as tk
import tkinter.ttk as ttk


class TreeView:
    def __init__(self, container):
        self.treeview = ttk.Treeview(container)
        self.sb_treeview = tk.Scrollbar(container)
        self.treeview.config(yscrollcommand=self.sb_treeview.set)
        self.sb_treeview.config(command=self.treeview.yview)

    def add_values(self, values, name):  # metoda wstawiająca nowe drzewo z gałęzią
        value = self.treeview.insert("", 'end', name, text=name)  # dodanie nowego drzewa (korzenia głównego)
        for i in values:
            self.treeview.insert(value, 'end', i, text=i)  # dodawanie kolejnych gałęzi drzewa

    def add_items(self, iid, values):  # dodawanie podgałęzi do istniejącej gałęzi drzewa
        for i in values:
            self.treeview.insert(iid, 'end', i, text=i)  # dodawanie podgałęzi drzewa