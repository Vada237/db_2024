from typing import Union

import psycopg2

from settings import db_connection, SAMPLES_TABLE_NAME, DESCRIPTIONS_TABLE_NAME, RANKS_TABLE_NAME, TAXONOMY_TABLE_NAME, \
    ROW_COUNT


class Repository:
    """
    Класс-хранилище запросов для выборки данных из бд
    """
    __connection = None

    @staticmethod
    def init():
        """
        Инициализация свойства с подключением
        """
        with psycopg2.connect(**db_connection) as conn:
            Repository.__connection = conn

    @staticmethod
    def get_descriptions(offset: int = 0):
        """
        Получение всех description с названием сэмплов
        """
        return Repository.__execute_select_query(f'''
            SELECT 
                d.id, s.name, d.location, d.coordinates_x, d.coordinates_y,
                d.soil_type, d.elevation, d.depth, d.body_site, d.temperature, d.ph
            FROM {DESCRIPTIONS_TABLE_NAME} as d
            INNER JOIN {SAMPLES_TABLE_NAME} as s on d.sample_id = s.id
            ORDER BY d.id ASC
            LIMIT {ROW_COUNT} OFFSET {offset * ROW_COUNT}
            ''')

    @staticmethod
    def get_ranks(offset: int = 0):
        """
        Получение всех ranks с названием таксономий и сэмплов
        """
        return Repository.__execute_select_query(f'''
            SELECT r.id, s.name, t.name, r._kingdom, r._phylum, r._class, r._order, r._family, r._genus
            FROM {RANKS_TABLE_NAME} as r
            INNER JOIN {TAXONOMY_TABLE_NAME} as t on t.id = r.taxonomy_id
            INNER JOIN {SAMPLES_TABLE_NAME} as s on s.id = t.sample_id
            ORDER BY r.id ASC
            LIMIT {ROW_COUNT} OFFSET {offset * ROW_COUNT}
        ''')

    @staticmethod
    def get_taxonomy_names():
        """
        Получение всех таксономий
        """
        return Repository.__execute_select_query(f'''SELECT DISTINCT(name) FROM {TAXONOMY_TABLE_NAME}''')

    @staticmethod
    def get_taxonomy_id_by_name_and_sample_id(taxonomy_name: str, sample_id: int):
        """
        Получить название таксономии по названию и сэмплу
        """
        return Repository.__execute_select_query(
            f'''SELECT id FROM {TAXONOMY_TABLE_NAME} WHERE name = %s and sample_id = %s''',
            True,
            (taxonomy_name, sample_id, )
        )

    @staticmethod
    def get_samples():
        """
        Получение всех samples
        """
        return Repository.__execute_select_query(f'''SELECT * FROM {SAMPLES_TABLE_NAME}''')

    @staticmethod
    def create_description(params: tuple) -> None:
        """
        Создать информацию об образце
        """
        return Repository.__execute_other_query(f'''
        INSERT INTO {DESCRIPTIONS_TABLE_NAME} (
        sample_id, location, coordinates_x, coordinates_y, soil_type, elevation, depth, body_site, temperature, ph 
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', params)

    @staticmethod
    def create_rank(params: tuple):
        """
        Создать rank
        """
        return Repository.__execute_other_query(f'''
        INSERT INTO {RANKS_TABLE_NAME} (taxonomy_id, _Kingdom, _Phylum, _Class, _Order, _Family, _Genus) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (_Kingdom, _Phylum, _Class, _Order, _Family, _Genus) DO NOTHING
        ''', params)

    @staticmethod
    def update_description_by_id(_id: int, params: list) -> None:
        """
        Обновить информацию по id
        """
        Repository.__execute_other_query(f'''
        UPDATE {DESCRIPTIONS_TABLE_NAME}
        SET sample_id = %s, location = %s, coordinates_x = %s, coordinates_y = %s,
        soil_type = %s, elevation = %s, depth = %s, body_site = %s, temperature = %s, ph = %s
        WHERE id = %s
        ''', tuple(params + [_id]))

    @staticmethod
    def update_rank_by_id(_id: int, params: tuple) -> None:
        """
        Обновить ранг по id
        """
        Repository.__execute_other_query(
            f'''
            UPDATE {RANKS_TABLE_NAME} SET 
            taxonomy_id = %s, _Kingdom = %s, _Phylum = %s, _Class = %s, 
            _Order = %s, _Family = %s, _Genus = %s
            WHERE id = %s AND NOT EXISTS (
            SELECT 1 FROM {RANKS_TABLE_NAME} WHERE taxonomy_id = %s AND _Kingdom = %s AND _Phylum = %s AND _Class = %s
            AND _Order = %s AND _Family = %s AND _Genus = %s
            )
            ''', (params[0], params[1], params[2], params[3], params[4], params[5], params[6],
                  _id, params[0], params[1], params[2], params[3], params[4], params[5], params[6])
        )

    @staticmethod
    def delete_by_id(_id: int, table_name: str) -> None:
        """
        Удалить запись с таблицы по id
        """
        Repository.__execute_other_query(f'''DELETE FROM {table_name} WHERE id = %s''', (_id,))

    @staticmethod
    def get_by_id(_id: int, table_name: str) -> tuple:
        """
        Получить запись с таблицы по id
        """
        return Repository.__execute_select_query(f'''SELECT * FROM {table_name} WHERE id = {_id}''', True)

    @staticmethod
    def get_count_rows(table_name: str) -> int:
        """
        Получить количество записей в таблице
        """
        return Repository.__execute_select_query(f'''SELECT count(*) FROM {table_name}''', True)[0]

    @staticmethod
    def __execute_select_query(query: str, get_first_row: bool = False, params=None) -> Union[list[tuple], tuple, None]:
        """
        Функция выполняющая запрос на выборку, была написана для избежания дублирующегося кода
        """
        with Repository.__connection.cursor() as cursor:
            cursor.execute(query) if not params else cursor.execute(query, params)

            return cursor.fetchall() if not get_first_row else cursor.fetchone()

    @staticmethod
    def __execute_other_query(query: str, params: tuple) -> None:
        """
        Функция выполняющая запрос на вставку, обновление и удаление, была написана для избежания дублирующегося кода
        """
        with Repository.__connection.cursor() as cursor:
            cursor.execute(query, params)
            Repository.__connection.commit()
