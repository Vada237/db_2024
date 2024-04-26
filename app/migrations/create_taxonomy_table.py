from app.migrations.migration import Migration
from settings import TAXONOMY_TABLE_NAME, SAMPLES_TABLE_NAME


class CreateTaxonomyTable:
    @staticmethod
    def run():
        Migration.run(f'''
        CREATE TABLE {TAXONOMY_TABLE_NAME} (
        id serial PRIMARY KEY,
        sample_id integer REFERENCES {SAMPLES_TABLE_NAME}(id) ON DELETE CASCADE ON UPDATE CASCADE,
        name text
        )
        ''')
