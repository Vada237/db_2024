import os
from typing import Union

import numpy as np
import pandas
import psycopg2

from app.parser.parser import Parser
from settings import DEFAULT_TAXONOMY, db_connection, TAXONOMY_TABLE_NAME, RANKS_TABLE_NAME


class RankParser(Parser):
    def _parse_data(self, filepath: Union[str, os.PathLike[str]] = None) -> Union[list[tuple], None]:
        df = pandas.read_csv(filepath).replace({np.nan: None})
        taxonomy_id = None
        _filepath = str(filepath)

        for taxonomy in DEFAULT_TAXONOMY:
            if taxonomy in _filepath:
                taxonomy_id = self.__get_taxonomy_id_by_name(taxonomy)
                break

        result = []
        for index, row in df.iterrows():
            result.append((taxonomy_id, row.get('Kingdom'), row.get('Phylum'),
                           row.get('Class'), row.get('Order'), row.get('Family'), row.get('Genus')))

        return result

    def _write_to_db(self, data: any) -> None:
        with psycopg2.connect(**db_connection) as conn:
            cursor = conn.cursor()
            cursor.executemany(f'''
            INSERT INTO {RANKS_TABLE_NAME} (taxonomy_id, _Kingdom, _Phylum, _Class, _Order, _Family, _Genus) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (_Kingdom, _Phylum, _Class, _Order, _Family, _Genus) DO NOTHING
            ''', data)
            conn.commit()

    @staticmethod
    def __get_taxonomy_id_by_name(taxonomy_name: str) -> int:
        with psycopg2.connect(**db_connection) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''SELECT id FROM {TAXONOMY_TABLE_NAME} where name = %s''', (taxonomy_name,))
            _id = cursor.fetchone()

            return _id[0]
