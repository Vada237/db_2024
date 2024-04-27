from app.migration_manager import MigrationManager
from app.migrations.migration import Migration
from app.parser_manager import ParserManager
from settings import enable_migration, need_refresh, enable_parser


def main():
    Migration.init()
    parser_manager = ParserManager()

    if enable_migration:
        MigrationManager.run_migrations()
    elif need_refresh:
        MigrationManager.refresh()

    if enable_parser:
        parser_manager.start()


if __name__ == '__main__':
    main()
