import psycopg2

from settings import db_connection, SAMPLES_TABLE_NAME, DESCRIPTIONS_TABLE_NAME, RANKS_TABLE_NAME, TAXONOMY_TABLE_NAME


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
    def get_descriptions():
        """
        Получение всех description с названием сэмплов
        """
        return Repository.__execute_select_query(f'''
            SELECT 
                d.id, s.name, d.location, d.coordinates_x, d.coordinates_y,
                d.soil_type, d.elevation, d.depth, d.body_site, d.temperature, d.ph
            FROM {DESCRIPTIONS_TABLE_NAME} as d
            INNER JOIN {SAMPLES_TABLE_NAME} as s on d.sample_id = s.id
            ''')

    @staticmethod
    def get_ranks(offset: int = 0):
        """
        Получение всех ranks с названием таксономий и сэмплов
        """
        return Repository.__execute_select_query(f'''
            SELECT r.id, r.name, r.value, t.name, s.name
            FROM {RANKS_TABLE_NAME} as r
            INNER JOIN {TAXONOMY_TABLE_NAME} as t on t.id = r.taxonomy_id
            INNER JOIN {SAMPLES_TABLE_NAME} as s on s.id = t.sample_id
            LIMIT 10 OFFSET {offset}
        ''')

    @staticmethod
    def __execute_select_query(query: str):
        """
        Функция выполняющая запрос, была написана для избежания дублирующегося кода
        """
        with Repository.__connection.cursor() as cursor:
            cursor.execute(query)

            return cursor.fetchall()
