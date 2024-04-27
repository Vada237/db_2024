from app.migrations.migration import Migration
from settings import DESCRIPTIONS_TABLE_NAME, SAMPLES_TABLE_NAME


class CreateDescriptionTable:
    @staticmethod
    def run():
        """
        Создание таблицы descriptions
        """

        Migration.run(f'''
        CREATE TABLE {DESCRIPTIONS_TABLE_NAME} (
        id serial PRIMARY KEY,        
        sample_id integer REFERENCES {SAMPLES_TABLE_NAME}(id) ON DELETE CASCADE ON UPDATE CASCADE,
        location text,
        coordinates_x float,
        coordinates_y float,
        soil_type text NULL,
        elevation integer NULL,
        depth float,
        body_site text NULL,
        temprerature float,
        pH float NULL
        )
        ''')
