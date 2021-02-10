import tkinter as tk
from tkinter.messagebox import showinfo

# import controller as ctrl
from GUI import GUI


class TworzeniekontaGUI(GUI):
    def __init__(self, controller):
        super().__init__(controller)
        self.loggingFrame = None
        self.loginEntry = None
        self.passwordEntry = None
        self.passwordEntry2 = None

    def printGUI(self):
        super().printGUI()
        font = ('TkDefaultFont', 15)
        self.loggingFrame = tk.Frame(self.window)
        self.loginEntry = tk.Entry(self.loggingFrame, font=font)
        self.passwordEntry = tk.Entry(self.loggingFrame, show="*", font=font)
        self.passwordEntry2 = tk.Entry(self.loggingFrame, show="*", font=font)
        tk.Label(self.window, text="Utwórz nowe konto w aplikacji tworząc swój login i hasło", font=font).pack(padx=20, pady=30)
        tk.Label(self.loggingFrame, text="Login", font=font).grid(column=0, row=0)
        self.loginEntry.grid(column=1, row=0)
        tk.Label(self.loggingFrame, text="Hasło", font=font).grid(column=0, row=1)
        self.passwordEntry.grid(column=1, row=1)
        tk.Label(self.loggingFrame, text="Powtórz hasło", font=font).grid(column=0, row=2)
        self.passwordEntry2.grid(column=1, row=2)
        self.loggingFrame.pack(padx=20, pady=20)

        buttonNewAccount = tk.Button(self.window, text="Stwórz konto", font=font, command=self.tworzenieKonta)
        buttonNewAccount.pack(side=tk.TOP, pady=10)
        buttonBack = tk.Button(self.window, text="Wróć", font=font, command=self.powrot)
        buttonBack.pack(side=tk.BOTTOM, pady=20)

        self.window.mainloop()

    def tworzenieKonta(self):
        login = self.loginEntry.get()
        haslo1 = self.passwordEntry.get()
        haslo2 = self.passwordEntry2.get()
        self.controller.tryNewAccount(login, haslo1, haslo2)

    def powrot(self):
        self.controller.showLoggingGUI()

    def infoboxOK(self, login):
        showinfo("Konto utworzone", "Konto " + login + " zostało utworzone!")

    def infoboxBadLogin(self, login):
        showinfo("Login zajęty", "Podany login (" + login + ") jest już zajęty.\nSpróbuj podać inny login.")

    def infoboxBadPassword(self):
        showinfo("Popraw hasło", "Wprowadzone hasła nie są identyczne!")
