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
  
 Схематически решение можно представить в виде диаграмы:
  
![case_1_message_broker](https://user-images.githubusercontent.com/1698696/111184594-28d30600-85c2-11eb-872f-ee6f4a0c5499.jpg)

generator - создает поток файлов с разным содержимым на диск
file_check - получает список файлов, лежащих в дирекории. Список полученных файлов отправляется в очередь брокера со списком файлов
file_get - из очерди со списком файлов брокера получает имя файла, читает кусок его содержимого и отправляет полученный результат в очередь "Очередь с данными из словарей" в брокере сообщений
save_to_db - получает сообщения из очереди "Очередь с данными из словарей" и сохраняет полученный данные в БД SQLite. В случае, если запись завершилась успешно данные об этом поемщается в очередь "Успешных операций", в противном случае - в очередь "Операций с ошибкой"
file_updater - получает сообщения из очереди "успешные операции", получает имя файла, данные которого было успешно сохранены. После этого удаляет из файла сохраненные в БД строки
 
Преимущества:
- масштабируемость - можно без ограничений запустить несколько сервисов выполняющих одну и ту же функциональность для ускорения скорости работы
- распределенность - брокер сообщений и часть сервисов системы могут быть вынесены на удаленные узлы
- стабильность - есть возможность реализовать обрабоку сценариев, в случае сбоя одного из сервисов без потери целостности данных 

Недостатки:
- сложность в эксплуатации и разработке

## Вариант решения №2: Использование каналов для обмена данными между сервисами

Решение основано на цикле операций, которые выполняются пока в директория, содержащая файлы непуста.
Цикл состоит из следующих операций:
- получается список файлов директории
- для каждого из файла запускается дочерний процесс, который берет заданное число строк из файла и возвращает в родительский процесс словарь, построенный на основе считанных строк
- Полученные словари сохраняются в БД
- В случае успешной операции записи словаря в БД создаются дочерние процессы для удаления "обработанных" строк из файла. В случае, если в файле не осталось строк, файл удаляется

Порядок действий при сбое или неожиданном завершении:
- В случае сбоя при обработке данных дочерним процессов - анализ и сохранение данных для конкретного файла прекращается, процедуру по анализу и обработке данных можно запустить повторно
- В случае сбоя при сохранении данных в БД SQLite - выполняется операция rollback на уровне базы данных
- В случае сбоя или неожиданного завершения родительского процесса - процесс можно запустить повтороно без потери данных (при запуске необходимо выставить парвильное значение переменных запуска, чтобы не выполнялось удаление БД )

Преимущество:
- простота реализации
- надежность - так как удаление данных происходит только после успешного созранения данных в базу - в случае сбоя или неожиданной остановки программы можно заново перезапустить программу и продолжить прерванный процесс

Недостатки:
- создает большое количество дочерних процессов

## Вариант решения №3: Использование очереди на базе брокера с дополнительным хранением сгенерированных файлов в виде фрагментированных кусочков

В целом вараинт повторяет вариант №1, но добавляется еще один этап.
Каждый исходный файл, который был сгенерирвоан утилитой generator делится на набор "фрагментирвоанных" файлов, размер которых ограничен заданным нами значением.
Дальнейшие действия по анализу данных производится на наборе "фрагментирвоанных" файлов.
Так же, в отличие варианта №1 утилита file_updater вместе удаления строк из файла может удалять файл целиком.

Преимущество:
- упрощение логики обработки файлов

Недостатки:
- дополнительные дисковые операции при для "фрагментирования" и копирования файлов
