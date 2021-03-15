# file-checker
Сервис для генерации набора файлов, их анализа и записи содержимого в БД для хранения.
Данный сервис решает задачу, описанную ниже

# Постановка задачи

Имеется сервис, генерирующий поток файлов с данными. Файлы записываются на диск. Размер файлов сильно варьируется: от десятков мегабайт до нескольких тысяч мегабайт.
Внутри каждого файла содержатся строки вида “123 12345”. Первое число – идентификатор потребителя, второе - количество потреблённого ресурса. В качестве разделителя используется пробел.
Поток файлов необходимо обрабатывать, суммируя количество ресурса по каждому отдельному потребителю. Итоговые данные нужно складывать в центральное хранилище, увеличивая имеющиеся там значения.

## Задачи

    1. Описать два-три способа надёжной и целостной обработки таких потоков файлов. Текстовое описание каждого способа должно предусматривать:
        a. способ передачи файла в инстанс/инстансы программы-обработчика;
        b. способ обработки файла внутри программы-обработчика;
        c. порядок реакции на неожиданное завершение программы-обработчика из-за непредвиденного сбоя.
    2. Написать программу, работающую по одному из описанных алгоритмов.
    3. Написать программу, генерирующую файлы с нужным содержимым.

Анализируя полученную задачу, стоит выделить следюущие ключеые моменты, ответы на которые необходимо найти для решения задачи:
### Ключевые моменты
  1. Как недежно передавать данные между несколькими программами / инстансами обработчика
  2. Как исключить потерю данных при неожиданном завершении одного их приложений
  3. Как гарантировать корректность работы приложения при обработке файла вне зависимости от размера файла. 
  
  # Решение
  
  ## Вариант решения №1: Использование очереди сообщений на базе брокера
  
  Решение основано на том, что каждый сервис выполняет свою часть работы получая данные из соответсувющей очереди брокера собщений. Результат, полученный в ходе своей работы передается так же в отдельную чоередь сообщений, котроая будет использована другим типом сервиса. 
