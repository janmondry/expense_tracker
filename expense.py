from datetime import datetime
import json


class Expense:
    def __init__(self, name, category, amount, date, iden=None, howManyParticipants=1):
        if iden is None:
            self.__id = None
        else:
            self.__id = iden
        self.__name = name
        self.__category = category
        self.__amount = float(amount)
        if type(date) == str:
            self.__date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            self.__date = date.date()
        self.__howManyParticipants = howManyParticipants

    @property
    def getID(self):
        return self.__id

    def setID(self, i):
        self.__id = i

    @property
    def getName(self):
        return self.__name

    @property
    def getCategory(self):
        return self.__category

    @property
    def getAmount(self):
        return self.__amount

    @property
    def getDate(self):
        return self.__date

    def getDict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "category": self.__category,
            "value": self.__amount,
            "date": str(self.__date)
        }

    @classmethod
    def fromDict(cls, dic):
        name = dic["name"]
        category = dic["category"]
        amount = float(dic["value"])
        date = datetime.strptime(dic["date"], '%Y-%m-%d')
        id = int(dic['id'])
        return cls(name, category, amount, date, id)

    def __str__(self):
        return self.__category + '\t' + self.__name + "\t" + str(self.__amount) + '\t' + str(self.__date)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __lt__(self, other):
        dzien1 = int(str(self.__date)[7:])
        dzien2 = int(str(other.getDate)[7:])
        return dzien1 < dzien2
