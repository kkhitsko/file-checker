__author__ = "Khitsko Konstantin <khitsko.konstantin@gmail.com>"
__date__ = "14.03.2021"

"""
Абстрактный класс для хранения данных
"""


class Storage:

    def commit(self):
        pass

    def rollback(self):
        pass

    def incrementValueByKey(self, key, value):
        pass

    def getValueByKey(self, key):
        pass

    def getCount(self):
        pass

    def clearAll(self):
        pass
