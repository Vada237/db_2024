from abc import ABC

import psycopg2

from settings import db_configuration


class Migration:
    __connection = None

    @staticmethod
    def init():
        with psycopg2.connect(**db_configuration) as conn:
            Migration.__connection = conn

    @staticmethod
    def run(query: str) -> None:
        with Migration.__connection.cursor() as cursor:
            cursor.execute(query)
            Migration.__connection.commit()

    @staticmethod
    def drop_all_tables() -> None:
        with Migration.__connection.cursor() as cursor:
            cursor.execute(f'''DROP SCHEMA public CASCADE;''')
            cursor.execute(f'''CREATE SCHEMA public;''')
            Migration.__connection.commit()
