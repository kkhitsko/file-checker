__author__ = "Khitsko Konstantin <khitsko.konstantin@gmail.com>"
__date__ = "14.03.2021"

import sqlite3
from Storage import Storage

"""
Класс для хранения данных в БД SQLite
"""


class SQLiteStorage(Storage):

    connection = None
    db_file = None

    _create_table_sql = """
    CREATE TABLE IF NOT EXISTS consumer (
        id INTEGER PRIMARY KEY,
        resource INTEGER
    )
    """

    _get_consumer_resource_value_sql = """
    SELECT resource FROM consumer WHERE id=?
    """

    _incr_consumer_resource_value_sql = """
    UPDATE consumer SET resource = ? where id = ?  
    """

    _insert_consumer_resource_value_sql = """
    INSERT INTO consumer VALUES (?,?)
    """

    _get_consumer_count_sql = """
    SELECT count(*) FROM consumer
    """

    _delete_all_from_consumer_sql = """
    DELETE FROM consumer
    """

    def __init__(self, db_file):
        self.db_file = db_file

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            cursor = self.connection.cursor()

            # При подключнии проверяем, есть ли таблица с данными
            # при необходимости ее создаем
            cursor.execute(self._create_table_sql)
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)

    def close(self):
        if self.connection:
            self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def incrementValueByKey(self, key, value):
        curr_value = self.getValueByKey(key)
        cursor = self.connection.cursor()
        if curr_value:
            value += curr_value
            cursor.execute(self._incr_consumer_resource_value_sql, [value, key])
        else:
            cursor.execute(self._insert_consumer_resource_value_sql, [key, value])
        cursor.close()

    def getValueByKey(self, key):
        value = None
        cursor = self.connection.cursor()

        cursor.execute(self._get_consumer_resource_value_sql, [key])
        res = cursor.fetchall()
        for row in res:
            return int(row[0])
        return value

    def getCount(self):
        value = None
        cursor = self.connection.cursor()

        cursor.execute(self._get_consumer_count_sql)
        res = cursor.fetchall()
        for row in res:
            return int(row[0])
        return value

    def clearAll(self):
        cursor = self.connection.cursor()
        cursor.execute(self._delete_all_from_consumer_sql)
        self.commit()
