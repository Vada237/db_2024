from typing import Union

import psycopg2

from app.parser.parser import Parser
from settings import db_connection, SAMPLES_TABLE_NAME, DEFAULT_TAXONOMY


class TaxonomyParser(Parser):
    def _parse_data(self, filepath: str = None) -> list[tuple]:
        data_to_insert = []
        sample_ids = self.__get_sample_ids()
        for taxonomy in DEFAULT_TAXONOMY:
            for sample_id in sample_ids:
                data_to_insert.append((sample_id, taxonomy))

        return data_to_insert

    def _write_to_db(self, data: any) -> None:
        super()._write_to_db(data)

    @staticmethod
    def __get_sample_ids() -> list[int]:
        with psycopg2.connect(**db_connection) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            SELECT id FROM {SAMPLES_TABLE_NAME}
            ''')

            data = cursor.fetchall()
            if data is not None:
                result = [row[0] for row in data]

                return result

            return []
