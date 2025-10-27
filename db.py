"""
Модуль db.py — работа с базой данных MySQL.
Содержит класс DB для подключения, добавления и обновления данных пользователей.
"""

import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class DB:
    """
    Класс для подключения к базе данных MySQL и выполнения операций с таблицей пользователей.
    """
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        """
        Инициализирует параметры подключения к базе данных.
        Args:
            host (str): Адрес сервера базы данных.
            user (str): Имя пользователя базы данных.
            password (str): Пароль пользователя.
            database (str): Имя базы данных.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        """
        Устанавливает соединение с базой данных MySQL.
        Raises:
            mysql.connector.Error: Если не удалось подключиться.
        """
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.cursor = self.connection.cursor()

    def add_person(self, person_id: int, name: str,
                   date_birth: str) -> None:
        """
        Добавляет нового пользователя в таблицу.

        Args:
            person_id (int): Уникальный идентификатор пользователя.
            name (str): Имя пользователя.
            date_birth (str): Дата рождения пользователя в формате YYYY-MM-DD.
        """
        sql = '''INSERT INTO hb (id, name, date_birth) VALUES (%s, %s, %s)'''
        values = (person_id, name, date_birth)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, values)
            self.connection.commit()
            print('Данные добавлены')
        except Exception as e:
            values = (person_id, name, date_birth)


    def update_person_date(self, person_id: int, name: str,
                           date_birth: str) -> None:
        """
        Обновляет дату рождения пользователя по его ID и имени.
                Args:
            person_id (int): Уникальный идентификатор пользователя.
            name (str): Имя пользователя.
            date_birth (str): Новая дата рождения пользователя в формате YYYY-MM-DD.
        """
        sql = '''UPDATE hb SET date_birth = %s WHERE id = %s AND name = %s'''
        values = (date_birth, person_id, name)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, values)
            self.connection.commit()
            print('Данные обновлены')
        except Exception as e:
            print(f'Ошибка обновления данных: {e}')

if __name__ == "__main__":
    db = DB(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    db.connect()
    db.add_person(5, 'Ксения', '1995-10-27')