import psycopg2
import psycopg2 as psql
from psycopg2 import pool

import atexit
import Client_Credentials


class PSQLConnection:
    _connection = None
    _cursor = None

    @staticmethod
    def connect() -> None:
        PSQLConnection._connection = psycopg2.connect(
            user=Client_Credentials.user,
            password=Client_Credentials.password,
            host=Client_Credentials.hostname,
            port=Client_Credentials.db_port,
            database=Client_Credentials.db
        )

        if PSQLConnection._connection:
            print(f"connected to {Client_Credentials.db} DB successfully")

        PSQLConnection._cursor = PSQLConnection._connection.cursor()

    @staticmethod
    def do(query: str, params: tuple = ()) -> None:
        """
        This method is meant for modifying the DB.
        """
        PSQLConnection._cursor.execute(query, params)
        PSQLConnection._connection.commit()
        print("done!")

    @staticmethod
    def get_group(query: str, params: tuple = ()):
        """
        This method is meant for returning values from the DB.
        """
        PSQLConnection._cursor.execute(query, params)
        PSQLConnection._connection.commit()
        print("grabbed!")
        return PSQLConnection._cursor.fetchall()

    @staticmethod
    def get(query: str, params: tuple = ()):
        """
        This method is meant for returning a value from the DB.
        """
        PSQLConnection._cursor.execute(query, params)
        PSQLConnection._connection.commit()
        print("grabbed!")
        return PSQLConnection._cursor.fetchone()

    @staticmethod
    def end() -> None:
        PSQLConnection._cursor.close()
