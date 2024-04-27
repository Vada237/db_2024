from app.migrations.create_description_table import CreateDescriptionTable
from app.migrations.create_ranks_table import CreateRanksTable
from app.migrations.create_sample_table import CreateSampleTable
from app.migrations.create_taxonomy_table import CreateTaxonomyTable
from app.migrations.migration import Migration


class MigrationManager:
    @staticmethod
    def run_migrations():
        """
        Запуск миграций, осторожнее с порядком
        """
        CreateSampleTable.run()
        CreateDescriptionTable.run()
        CreateTaxonomyTable.run()
        CreateRanksTable.run()

    @staticmethod
    def refresh():
        """
        Рестарт миграций
        """
        Migration.drop_all_tables()
        MigrationManager.run_migrations()
