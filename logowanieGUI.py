from tkinter.messagebox import showinfo

from GUI import GUI
import tkinter as tk


class LogowanieGUI(GUI):
    def __init__(self, controller):
        super().__init__(controller)
        self.loggingFrame = None
        self.loginEntry = None
        self.passwordEntry = None

    def printGUI(self):
        super().printGUI()
        font = ('TkDefaultFont', 15)
        self.loggingFrame = tk.Frame(self.window)
        self.loginEntry = tk.Entry(self.loggingFrame, font=font)
        self.passwordEntry = tk.Entry(self.loggingFrame, show="*", font=font)
        tk.Label(self.window, text="Witaj w aplikacji ExpenseTracker!", font=font).pack(padx=20, pady=30)  # Create a text label
        # label# Pack it into the window
        tk.Label(self.window, text="Zaloguj się do aplikacji lub utwórz nowe konto", font=font).pack(pady=(0, 30))
        tk.Label(self.window, text="Przykładowe dane logowania:\nLogin: login1\nHasło: haslo1", font=font).pack(pady=(0, 30))
        # self.loggingframe = tk.Frame(self.window)
        tk.Label(self.loggingFrame, text="Login", font=font).grid(column=0, row=0)
        self.loginEntry.grid(column=1, row=0)
        tk.Label(self.loggingFrame, text="Hasło", font=font).grid(column=0, row=1)
        self.passwordEntry.grid(column=1, row=1)
        self.loggingFrame.pack(padx=20, pady=30)

        buttonLogin = tk.Button(self.window, text="Zaloguj się", font=font, command=self.logowanie)
        buttonLogin.pack(side=tk.TOP)
        tk.Label(self.window, text='lub', font=font).pack(side=tk.TOP, pady=20)
        buttonNewAccount = tk.Button(self.window, text="Utwórz nowe konto", font=font, command=self.tworzenieKonta)
        buttonNewAccount.pack(side=tk.TOP)

        self.window.mainloop()

    def tworzenieKonta(self):
        self.controller.showNewAccountGUI()

    def logowanie(self):
        login = self.loginEntry.get()
        password = self.passwordEntry.get()
        self.controller.tryToLogin(login, password)

    def infoboxBadLoginOrPassword(self):
        showinfo("Błąd logowania", "Wprowadzono niepoprawne dane logowania!")

    def infoboxLoggingOK(self):
        showinfo("Zalogowano", "Logowanie zakończone pomyślnie!")