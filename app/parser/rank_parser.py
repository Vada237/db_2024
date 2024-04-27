import os
from typing import Union

import pandas
import psycopg2

from app.parser.parser import Parser
from settings import DEFAULT_TAXONOMY, db_connection, TAXONOMY_TABLE_NAME, RANKS_TABLE_NAME


class RankParser(Parser):
    def _parse_data(self, filepath: Union[str, os.PathLike[str]] = None) -> Union[list[tuple], None]:
        df = pandas.read_csv(filepath)
        taxonomy_id = None
        _filepath = str(filepath)

        for taxonomy in DEFAULT_TAXONOMY:
            if taxonomy in _filepath:
                taxonomy_id = self.__get_taxonomy_id_by_name(taxonomy)
                break

        result = []
        headers = df.columns[1:]
        for header in headers:
            values = df[header].dropna().unique().tolist()
            for value in values:
                result.append((taxonomy_id, header, value))

        return result

    def _write_to_db(self, data: any) -> None:
        with psycopg2.connect(**db_connection) as conn:
            cursor = conn.cursor()
            cursor.executemany(f'''
            INSERT INTO {RANKS_TABLE_NAME} (taxonomy_id, name, value) VALUES (%s, %s, %s)
            ON CONFLICT (name, value) DO NOTHING
            ''', data)
            conn.commit()

    @staticmethod
    def __get_taxonomy_id_by_name(taxonomy_name: str) -> int:
        with psycopg2.connect(**db_connection) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''SELECT id FROM {TAXONOMY_TABLE_NAME} where name = %s''', (taxonomy_name, ))
            _id = cursor.fetchone()

            return _id[0]
