import os
from typing import Union

import numpy as np
import pandas
import psycopg2

from app.parser.parser import Parser
from settings import db_connection, DEFAULT_SAMPLES, SAMPLES_TABLE_NAME, DESCRIPTIONS_TABLE_NAME


class DescriptionParser(Parser):
    def _parse_data(self, filepath: str = None) -> Union[list[tuple], None]:
        result = []
        df = pandas.read_csv(filepath).replace(np.nan, None)
        sample_name = filepath.name.split('_')[0]
        sample_id = None
        for default_sample in DEFAULT_SAMPLES:
            if sample_name in default_sample:
                sample_id = DescriptionParser.__get_sample_id_by_name(sample_name)
                break

        for index, row in df.iterrows():
            result.append((
                sample_id, row.get('location'),
                row.get('coordinates x'), row.get('coordinates y'),
                row.get('soil_type'), row.get('elevation'),
                row.get('depth'), row.get('body_site'),
                row.get('temperature'), row.get('pH')
            ))

        return result

    def _write_to_db(self, data: any) -> None:
        with psycopg2.connect(**db_connection) as conn:
            cursor = conn.cursor()
            cursor.executemany(f"""
            INSERT INTO {DESCRIPTIONS_TABLE_NAME} (
            sample_id, location, coordinates_x, coordinates_y, soil_type, elevation, depth, body_site, temperature, ph
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, data)
            conn.commit()

    @staticmethod
    def __get_sample_id_by_name(sample_name: str) -> int:
        with psycopg2.connect(**db_connection) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""SELECT id FROM {SAMPLES_TABLE_NAME} where name ilike '%{sample_name}%' """)

            return cursor.fetchone()[0]
