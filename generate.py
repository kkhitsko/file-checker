__author__ = "Khitsko Konstantin <khitsko.konstantin@gmail.com>"
__date__ = "14.03.2021"

import argparse
import numpy
import time

"""
Скрипт для генерации набора файлов содержащих случайный набор
Внутри каждого файла содержатся строки вида “123 12345”. 
Первое число – идентификатор потребителя, второе - количество потреблённого ресурса. 
В качестве разделителя используется пробел.
"""


def prepareArgs():
    desc = "Утилита для генерации случайных файлов"
    args_parser = argparse.ArgumentParser(description=desc)
    args_parser.add_argument("-c", "--count", help="Число сгенерированных файлов",
                             dest="count", default="10", required=False)
    args_parser.add_argument("-l", "--lines", help="Максимальная количество строк файла",
                             dest="lines", default="100000", required=False)
    args_parser.add_argument("-k", "--max_consumer_id", help="Максимальный идентификатор потребителя",
                             dest="max_consumer_id", default="1000", required=False)
    args_parser.add_argument("-r", "--max_consumer_res_value", help="Максимальное назначение ресурса для потребителя",
                             dest="max_consumer_res_value", default="10000", required=False)
    return args_parser


def generateRandomFile(filename, args, lines_count):
    """
    Функция для генерации содержимого файла filename
    :param filename: Имя файла
    :type filename: str
    :param args: Параметры запуска скрипта
    :param lines_count: Число строк, которые должен содержать файл
    :return:
    """
    numbers_list = numpy.random.randint(0, int(args.max_consumer_id), lines_count)
    counters_list = numpy.random.randint(0, int(args.max_consumer_res_value), lines_count)
    with open(filename, "w") as outfile:
        for i in range(0, lines_count):
            outfile.write("{} {}\n".format(numbers_list[i], counters_list[i]))
    outfile.close()


def main():
    args_parser = prepareArgs()
    args = args_parser.parse_args()

    for i in range(0, int(args.count)):
        print("Генерируем файл: {}".format(i))
        filename = "data/file_{}_{}.txt".format(int(time.time()), i)
        # Генерируем файл с произвольным числом строк от 0 до args.lines
        generateRandomFile(filename, args, numpy.random.randint(int(args.lines)))


if __name__ == '__main__':
    main()
