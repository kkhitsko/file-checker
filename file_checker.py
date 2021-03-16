__author__ = "Khitsko Konstantin <khitsko.konstantin@gmail.com>"
__date__ = "14.03.2021"


import asyncio
import argparse
import time

from SQLiteStorage import SQLiteStorage
from FileChecker import FileChecker


def prepareArgs():
    desc = "Сервис для анализа содержимого файлов"
    args_parser = argparse.ArgumentParser(description=desc)
    args_parser.add_argument("-d", "--directory", help="Путь к директории со файлами для анализа",
                             dest="directory", default="data/", required=False)
    args_parser.add_argument("-t", "--timer", help="Период проверки файлов",
                             dest="timer", default="10", required=False)
    args_parser.add_argument("-c", "--chunk", help="Число строк, которые вычитываем за раз",
                             dest="chunk", default="1000", required=False)
    return args_parser


@asyncio.coroutine
def getConsumerData(fname, chunk):
    """
    Запускает процесс для получения содержимого первых
    строк файла в отдельном процессе
    :param fname: Имя файла
    :type fname: str
    :param chunk: Число строк для анализа
    :type chunk: int
    :return: Возвращает кортеж из буфера stdout скрипта, кода выполнения команды, имени файла
    """
    # Создаем процесс
    create = asyncio.create_subprocess_exec(
        'python3', 'get_file.py', fname, str(chunk), stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
    process = yield from create

    print("Создан процесс {} на чтение файла {}".format(process.pid, fname))

    # Ждем завершения процесса
    coroutine = process.communicate(input=None)
    output, _ = yield from asyncio.wait_for(coroutine, 10.0)

    if process.returncode != 0:
        print("Error {} while execute subprocess".format(process.returncode))
    else:
        print("Process {} successfully exited".format(process.pid))

    # Возвращаем ответ
    data = output.decode('utf-8')
    return data, process.returncode, fname


@asyncio.coroutine
def delFileLines(fname, chunk):
    """
    Запускает процесс удаления строк файла в отдельном процессе
    :param fname: Имя файла
    :type fname: str
    :param chunk: Число строк для удаления
    :type chunk: int
    :return: Возвращает кортеж из буфера stdout скрипта, кода выполнения команды, имени файла
    """

    # Создаем процесс
    create = asyncio.create_subprocess_exec(
        '/bin/bash', 'truncate_file.sh', fname, str(chunk), stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
    process = yield from create

    print("Создан процесс {} на удаление  строк файла {}".format(process.pid, fname))

    # Ждем завершения процесса
    coroutine = process.communicate(input=None)
    output, _ = yield from asyncio.wait_for(coroutine, 10.0)

    if process.returncode != 0:
        print("Error {} while execute subprocess".format(process.returncode))
    else:
        print("Process {} successfully exited".format(process.pid))

    # Возвращаем ответ
    data = output.decode('utf-8')
    return data, process.returncode, fname


def getDictFromOutput(output):
    """
    Функция принимает на вход буффер вывода запущенного скрипта и возвращает данные
    в виде словаря
    :param output: Буффер, содержащий вывод stdout запущеного скрипта
    :type output: str
    :return: Словарь содержащийся в выводе файла
    :rtype: dict
    """
    dict = {}
    values = output.split("\n")
    for val in values:
        tokens = val.split(" ")
        if len(tokens) == 2:
            dict[int(tokens[0])] = int(tokens[1])
    return dict


async def main():
    args_parser = prepareArgs()
    args = args_parser.parse_args()

    # TODO: Добавить параметр запуска с именем файла БД
    storage = SQLiteStorage("database.db")
    storage.connect()

    # При перовом запуске программы очищаем содержимое БД хранения

    storage.clearAll()

    # TODO: Предусмотреть то, что основаня программа в предыдущий раз
    #     могла завершиться с ошибкой. В таком случае очищать БД не стоит

    """
    Считаем число полученных из файлов записей
    Если число новых записей равно нулю выходим их цикла
    """
    new_consumers_cnt = 1

    # TODO: Реализовать таймер на asyncio
    while new_consumers_cnt > 0:
        new_consumers_cnt = 0

        checker = FileChecker(args)
        files = checker.getFilesList()

        tasks = []  # Таски на получение данных из файла
        del_tasks = []  # Таски на удаление строк из файла
        for file in files:
            tasks.append(getConsumerData(file, args.chunk))

        results = await asyncio.gather(*tasks)

        for res in results:
            if res[1] == 0:
                data = getDictFromOutput(res[0])
                print("Обрабатываем результат для файла {}".format(res[2]))
                try:
                    for key, values in data.items():
                        storage.incrementValueByKey(key, values)
                    storage.commit()
                    new_consumers_cnt += 1

                    # Создаем задачи для удаления успешно обработанных строк файла
                    del_tasks.append(delFileLines(res[2], int(args.chunk) + 1))
                except:
                    storage.rollback()
            else:
                print("Обработка файла {} завершилась ошибкой {}".format(res[2], res[1]))

        print("Число успешно обработанных файлов: {}".format(new_consumers_cnt))
        print("Число записей в таблице: {}".format(storage.getCount()))

        await asyncio.gather(*del_tasks)
        # TODO: Продумать, какие могут быть варианты некорректного
        #  завершения скрипта и реализовать обработку сценариев

        time.sleep(int(args.timer))

    storage.close()


if __name__ == '__main__':
    asyncio.run(main())
