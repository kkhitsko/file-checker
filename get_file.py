__author__ = "Khitsko Konstantin <khitsko.konstantin@gmail.com>"
__date__ = "14.03.2021"

import sys

"""
Скрипт для анализа содержимого файла
На входе получает имя файла и число строк для анализа
Выводит в stdout содержимое полученного словаря
"""


def main():

    data = {}

    with open(sys.argv[1]) as f:
        cnt = 0
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            consumer_id = 0
            consumer_value = 0
            tokens = line.split(" ")
            if len(tokens) == 2:
                consumer_id = int(tokens[0])
                consumer_value = int(tokens[1])

            if consumer_id in data.keys():
                data[consumer_id] += consumer_value
            else:
                data[consumer_id] = consumer_value

            cnt += 1
            if cnt >= int(sys.argv[2]):
                break
    f.close()
    for key, value in data.items():
        print(key, value)


if __name__ == '__main__':
    main()
