import expense as myExpense
import category as Category
import datetime


class User:
    static_count = 0

    def __init__(self, login, listOfExpenses=[]):
        self.__login = login
        self.__listOfExpenses = listOfExpenses

    def addExpense(self, exp):
        self.__listOfExpenses.append(exp)

    def delExpense(self, expID):
        for exp in self.__listOfExpenses:
            if exp.getID == expID:
                self.__listOfExpenses.remove(exp)

    def avgOverall(self):
        dictOfMonthsYears_avg = {}
        for exp in self.__listOfExpenses:
            monthyear = (exp.getDate.month, exp.getDate.year)
            if monthyear not in dictOfMonthsYears_avg.keys():
                dictOfMonthsYears_avg[monthyear] = (exp.getAmount, 1)
            else:
                old_avg, count = dictOfMonthsYears_avg[monthyear]
                new_avg = (old_avg * count + exp.getAmount) / (count + 1)
                dictOfMonthsYears_avg[monthyear] = (new_avg, count+1)
        sum_overall = 0
        count_overall = 0
        for monthyear in dictOfMonthsYears_avg.keys():
            month_avg, _ = dictOfMonthsYears_avg[monthyear]
            sum_overall += month_avg
            count_overall += 1
        if count_overall == 0:
            return 0
        else:
            return sum_overall/count_overall

    def avgMonth(self, month: int, year: int, category=None):
        suma = 0
        howMany = 0
        for exp in self.__listOfExpenses:
            if exp.date.month == month and exp.date.year == year and (exp.getCategory == category or category is None):
                suma += exp.amount
                howMany += 1
        return suma / howMany

    def avgToThisDay(self, day: int):
        dictOfMonthsYears_AvgToThisDay = {}
        for exp in self.__listOfExpenses:
            if exp.getDate.day <= day:
                monthyear = (exp.getDate.month, exp.getDate.year)
                if monthyear not in dictOfMonthsYears_AvgToThisDay.keys():
                    dictOfMonthsYears_AvgToThisDay[monthyear] = (exp.getAmount, 1)
                else:
                    old_avg, count = dictOfMonthsYears_AvgToThisDay[monthyear]
                    new_avg = (old_avg * count + exp.getAmount) / (count + 1)
                    dictOfMonthsYears_AvgToThisDay[monthyear] = (new_avg, count + 1)
        sumka = 0
        for k, _ in dictOfMonthsYears_AvgToThisDay.values():             # {(2, 2020): (2200.12, 4), ... }
            sumka += k
        return sumka/len(dictOfMonthsYears_AvgToThisDay)

    def getExpensesToToday(self):
        sumka = 0
        today = datetime.datetime.today()
        for exp in self.__listOfExpenses:
            if exp.getDate.month == today.month and exp.getDate.year == today.year and exp.getDate.day <= today.day:
                # TODO: tu skończyłem
                sumka += exp.getAmount
        return sumka

    @property
    def getLogin(self):
        return self.__login

    @property
    def getList(self):
        return self.__listOfExpenses
#
#
# user1 = User("login1", "pass1")
# user1.addExpense(myExpense.Expense("name1", Category.Category.cat1, 4.50, datetime.datetime.today, 1))
# print(user1)
