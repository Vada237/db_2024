import psycopg2

from app.parser.parser import Parser
from settings import db_connection, SAMPLES_TABLE_NAME


class SampleParser(Parser):
    def start_parse(self, filepath: str = None) -> None:
        self._write_to_db([('Sea soil',), ('Sea water',), ('Sea plant',)])

    def _write_to_db(self, data: list[tuple]) -> None:
        with psycopg2.connect(**db_connection) as conn:
            cursor = conn.cursor()
            cursor.executemany(f'''INSERT INTO {SAMPLES_TABLE_NAME} (name) VALUES (%s)''', data)
            conn.commit()
