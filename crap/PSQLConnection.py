import psycopg2
import psycopg2 as psql
from psycopg2 import pool

import atexit
import Client_Credentials


class PSQLConnection:
    def __init__(self):
        self._connection = psycopg2.connect(
            user=Client_Credentials.user,
            password=Client_Credentials.password,
            host=Client_Credentials.hostname,
            port=Client_Credentials.port,
            database=Client_Credentials.db
        )

        if self._connection:
            print(f"connected to {Client_Credentials.db} successfully")

        self._cursor = self._connection.cursor()

    def do(self, query: str, params: tuple = ()):
        self._cursor.execute(query, params)
        self._connection.commit()
        try:
            return self._cursor.fetchall()
        except psycopg2.ProgrammingError:
            print("executed!")

    def end(self):
        self._cursor.close()
