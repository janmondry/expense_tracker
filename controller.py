from datetime import datetime

import GUI
import Model
import tworzeniekontaGUI
import logowanieGUI
import zalogowanyGUI
from expense import Expense


class Controller:
    def __init__(self):
        self.model = None
        self.view = None

    def addModel(self, model):
        self.model = model

    def addView(self, view):
        self.view = view

    def tryToLogin(self, login, haslo):
        czyZalogowano = self.model.tryToLogin(login, haslo)
        if czyZalogowano:
            self.view.infoboxLoggingOK()
            self.showLoggedInGUI()
        else:
            self.view.infoboxBadLoginOrPassword()

    def tryNewAccount(self, login, haslo1, haslo2):
        if haslo1 == haslo2:
            res = self.model.tryNewAccount(login, haslo1)
            if res:
                self.view.infoboxOK(login)
                self.showLoggingGUI()
            else:
                self.view.infoboxBadLogin(login)
        else:
            self.view.infoboxBadPassword()

    def tryAddExpense(self, name, category, value, date):
        expense = Expense(name, category, value, date)
        # if type(name) is str and type(category) is str and type(value) is float and type(date) is datetime:
        #     print("xD")
        self.model.addExpense(expense)
        self.view.infoboxAddingOK()

    def showLoggingGUI(self):
        if self.view is not None:
            self.view.destroyGUI()
        self.view = logowanieGUI.LogowanieGUI(self)
        self.view.printGUI()

    def showNewAccountGUI(self):
        if self.view is not None:
            self.view.destroyGUI()
        self.view = tworzeniekontaGUI.TworzeniekontaGUI(self)
        self.view.printGUI()

    def showLoggedInGUI(self):
        if self.view is not None:
            self.view.destroyGUI()
        self.view = zalogowanyGUI.ZalogowanyGUI(self)
        self.view.printGUI()

    def getmonthyeardict(self):
        return self.model.getmonthyeardict()

    def getMonthYearToSumDict(self):
        return self.model.getMonthYearToSumDict()

    def deleteExpense(self, expense):
        if self.model is not None:
            self.model.deleteExpense(expense)

    def getAvgToDay(self, day):
        return self.model.getAvgToDay(day)

    def getExpensesToToday(self):
        return self.model.getExpensesToToday()

    def getAvgOfOthers(self):
        return self.model.getAvgOfOthers()

    def getAvgOverall(self):
        return self.model.getAvgOverall()

    def getCategoryToAmountDict(self):
        return self.model.getCategoryToAmountDict()

    def userHasNoHistory(self):
        return self.model.userHasNoHistory()
