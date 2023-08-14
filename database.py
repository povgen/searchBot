import sqlite3
from sqlite3 import Connection, Cursor


class Database:
    connection: Connection
    cursor: Cursor

    @classmethod
    def _connect(cls, db_name="main.db"):
        cls.connection = sqlite3.connect(db_name)
        cls.cursor = cls.connection.cursor()

    @classmethod
    def _disconnect(cls):
        cls.cursor.close()
        cls.connection.close()

    @classmethod
    def _insert_item(cls, table, data: dict):
        keys = data.keys()

        if not keys:
            return False

        cols = ', '.join(keys)
        vals = ', '.join(':' + col for col in keys)

        sql = f'INSERT INTO {table} ({cols}) VALUES ({vals})'
        return cls.execute(sql, data)

    @classmethod
    def _insert_list(cls, table, data: list):
        if len(data) == 0:
            return False

        keys = data[0].keys()
        rows = []
        params = {}
        columns = ', '.join(keys)

        for i, item in enumerate(data):
            row = []
            for column in item:
                print(column)
                params[f'{column}_{i}'] = item[column]
                row.append(f':{column}_{i}')

            row = ', '.join(row)
            rows.append(f'({row})')

        rows = ',\n'.join(rows)
        sql = f'INSERT INTO {table} ({columns}) VALUES \n{rows}'

        return cls.execute(sql, params)

    @classmethod
    def execute(cls, sql, params=None):
        if params is not None:
            result = cls.cursor.execute(sql, params)
        else:
            result = cls.cursor.execute(sql)

        cls.connection.commit()

        cls._disconnect()
        return result

    @classmethod
    def insert(cls, table, data: dict or list):
        return cls._insert_item(table, data) if type(data) is dict else cls._insert_list(table, data)
