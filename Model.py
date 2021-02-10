import json

from expense import Expense
from user import User
from hashlib import sha256
import pyrebase
from datetime import datetime


def hahahasz(string: str):
    return sha256(string.encode("utf-8")).hexdigest()


def configureDatabase():
    config = {
      "apiKey": "AIzaSyBw4rFOr-NJCdPkm8BbiKglFP9yemXtUek",
      "authDomain": "projekt-skryptowe.firebaseapp.com",
      "databaseURL": "https://projekt-skryptowe-default-rtdb.europe-west1.firebasedatabase.app/",
      "storageBucket": "projekt-skryptowe.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    database = firebase.database()
    # tak się dodaje dane do bazy jkbc
    # data = {"name": "Morty"}
    # db.child("users").set({"user1": "jan"})
    # db.child("users").child("user1").set({"loginpassword": hahahasz("login1haslo1"), "month_avg": 2100.23})
    # addUserToDB("login1", "haslo1", database)
    return database


def sortByDay(listOfExpenses: list):
    listOfExpenses.sort(reverse=True)
    return listOfExpenses


class Database:
    def __init__(self):
        self.database = configureDatabase()
        self.user = None

    def addUserToDB(self, login, password):
        self.database.child("users").child("user" + login).set(
            {"login": login,
             "password": hahahasz(password),
             "month_avg": 0})

    def getUserFromDB(self, login):
        userToReturn = None
        all_users = self.database.child("users").get()
        for u in all_users.each():
            usersDict = u.val()
            loginFromDB = usersDict["login"]
            if login == loginFromDB:
                if "listOfExpenses" in usersDict.keys():
                    # ten kawałek zapewnia, że pobrane z firebasa expensy są klasy Expense, a nie dict
                    lista = usersDict["listOfExpenses"]
                    listaToReturn = []
                    for exp in lista:
                        if type(exp) == dict:
                            listaToReturn.append(Expense.fromDict(exp))
                        elif exp is not None:           # TODO może dawać błędy, nwm
                            listaToReturn.append(exp)
                    # ---------------------------------------------------------------------------------
                    return User(usersDict["login"], listaToReturn)
                else:
                    return User(usersDict["login"])
        return userToReturn

    def addExpense(self, expense):
        if self.user is not None:
            if len(self.user.getList) != 0:
                newID = self.user.getList[-1].getID + 1
            else:
                newID = 0
            newID_str = str(newID)
            expense.setID(newID)
            self.user.addExpense(expense)
            data = expense.getDict()
            self.database.child("users").child("user"+self.user.getLogin).child("listOfExpenses").child(newID_str).update(data)
            self.database.child("users").child("user"+self.user.getLogin).update({"month_avg": self.user.avgOverall()})

    def deleteExpense(self, expenseDict):
        idUsuwanego = expenseDict['values'][3]
        id_str = str(idUsuwanego)
        # usuwana_wartosc = float(expenseDict['values'][2])
        # # nowa_śr = ((stara_śr * stara_ilosc) - usuwany) / nowa_ilosc
        # stara_srednia = float(self.database.child("users").child("user" + self.user.getLogin).child("month_avg").get().val())
        # stara_ilosc = len(self.user.getList)
        # nowa_ilosc = stara_ilosc - 1
        # if nowa_ilosc != 0:
        #     nowa_srednia = ((stara_srednia * stara_ilosc) - usuwana_wartosc) / nowa_ilosc
        # else:
        #     nowa_srednia = 0

        self.user.delExpense(idUsuwanego)
        self.database.child("users").child("user"+self.user.getLogin).child("listOfExpenses").child(id_str).remove()
        self.database.child("users").child("user" + self.user.getLogin).update({"month_avg": self.user.avgOverall()})

    def getUsersHashesListFromDB(self):
        listToReturn = []
        all_users = self.database.child("users").get()
        for user in all_users.each():
            usersDict = user.val()  # {name": "Mortimer 'Morty' Smith"}
            loginandpassword = (usersDict["login"], usersDict["password"])
            listToReturn.append(loginandpassword)
            # print(usersDict["loginpassword"])
        return listToReturn  # (login, hashedPassword)

    def tryToLogin(self, login, password):
        if self.czyDaneLogowaniaPoprawne(login, password):
            print("Zalogowano!")
            self.user = self.getUserFromDB(login)
            return True
        else:
            print("Sprobuj jeszcze raz")
            return False

    def czyDaneLogowaniaPoprawne(self, login, haslo):
        if login == "" or haslo == "":
            return False
        usersHashes = self.getUsersHashesListFromDB()
        for log, pwd in usersHashes:
            if pwd == hahahasz(haslo) and login == log:
                return True
        return False

    def czyIstniejeUser(self, login):
        usersHashes = self.getUsersHashesListFromDB()
        for log, _ in usersHashes:
            if login == log:
                return True
        return False

    def tryNewAccount(self, login, haslo):
        if self.czyIstniejeUser(login):
            return False
        else:
            self.addUserToDB(login, haslo)
            return True

    def getmonthyeardict(self):
        if self.user is not None:
            listOfExpenses = self.user.getList
            dictToReturn = {}       # {"<Month-year>": {<data1>: listaExpenses, <data2>: lista...}}
            for entry in listOfExpenses:
                dataEntry = entry.getDate
                monthyearEntry = str(dataEntry)[:7]
                if monthyearEntry in dictToReturn.keys():
                    if entry.getDate in dictToReturn[monthyearEntry].keys():
                        (dictToReturn[monthyearEntry])[entry.getDate].append(entry)
                    else:
                        (dictToReturn[monthyearEntry])[entry.getDate] = [entry]
                else:
                    dictToReturn[monthyearEntry] = {entry.getDate: [entry]}

            # to sortuje lata i miesiące odpowiednio
            dictToReturn = dict(sorted(dictToReturn.items(), reverse=True))

            # a to sortuje dni w miesiącolatach odpowiednio
            dictToReturn2 = {}
            for ym, dictOfDays in dictToReturn.items():
                sortedDictOfDays = dict(sorted(dictOfDays.items(), reverse=True))
                dictToReturn2[ym] = sortedDictOfDays
            # for listaExpenses in dictToReturn.values():
            #     sortByDay(listaExpenses)
            return dictToReturn2

        else:
            return {}

    def getMonthYearToSumDict(self):
        if self.user is not None:
            listOfExpenses = self.user.getList
            dictToReturn = {}       # {"<Month-year>": <suma1>, }
            for entry in listOfExpenses:
                dataEntry = entry.getDate
                monthyearEntry = str(dataEntry)[:7]
                if monthyearEntry in dictToReturn.keys():
                    dictToReturn[monthyearEntry] += entry.getAmount
                else:
                    dictToReturn[monthyearEntry] = entry.getAmount

            # to sortuje lata i miesiące odpowiednio
            dictToReturn = dict(sorted(dictToReturn.items(), reverse=True))
            return dictToReturn
        else:
            return {}

    def getAvgToDay(self, day):
        return self.user.avgToThisDay(day)

    def getExpensesToToday(self):
        return self.user.getExpensesToToday()

    def getAvgOfOthers(self):
        sumka = 0
        count = 0
        all_users = self.database.child('users').get().each()
        for u in all_users:
            usersDict = u.val()
            otherLogin = usersDict['login']
            if self.user.getLogin != otherLogin and usersDict['month_avg'] > 0:
                sumka += usersDict['month_avg']
                count += 1
        return sumka/count

    def getAvgOverall(self):
        return self.user.avgOverall()

    def getCategoryToAmountDict(self):
        dictToReturn = {}
        year, month = datetime.today().year, datetime.today().month
        for exp in self.user.getList:
            if exp.getDate.year == year and exp.getDate.month == month:
                cat = exp.getCategory
                if cat in dictToReturn.keys():
                    dictToReturn[cat] += exp.getAmount
                else:
                    dictToReturn[cat] = exp.getAmount
        return dictToReturn

    def userHasNoHistory(self):
        return len(self.user.getList) == 0
