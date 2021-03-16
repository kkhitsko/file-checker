__author__ = "Khitsko Konstantin <khitsko.konstantin@gmail.com>"
__date__ = "14.03.2021"

from os import listdir
from os.path import isfile, join

"""
Класс для работы с содержимом директоририи и получения и фильтрации списка файлов
"""
class FileChecker:

    files = []

    directory = None

    def __init__(self, args):
        self.directory = args.directory

    def getFilesList(self):
        try:
            print("Try to get files in directory: {}".format(self.directory))
            self.files = [join(self.directory, f) for f in listdir(self.directory) if isfile(join(self.directory, f))]
        except FileNotFoundError as error:
            print("Ошибка при получении списка файлов: {}".format(error))
        print("Directory {} contain {} files".format(self.directory, len(self.files)))
        return self.files
