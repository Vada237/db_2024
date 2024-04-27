from app.migration_manager import MigrationManager
from app.migrations.migration import Migration
from settings import enable_migration, need_refresh


def main():
    Migration.init()
    if enable_migration:
        MigrationManager.run_migrations()
    elif need_refresh:
        MigrationManager.refresh()


if __name__ == '__main__':
    main()
