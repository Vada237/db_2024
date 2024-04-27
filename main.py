from flask import Flask

from app.migration_manager import MigrationManager
from app.migrations.migration import Migration
from app.parser_manager import ParserManager


app = Flask(__name__)


@app.route('database/refresh', methods=['POST'])
def refresh_database():
    MigrationManager.refresh()


@app.route('database/migrate', methods=['POST'])
def start_migrate():
    MigrationManager.run_migrations()


@app.route('database/parse', methods=['GET'])
def start_parse():
    parser_manager.start()


if __name__ == '__main__':
    Migration.init()
    parser_manager = ParserManager()
    app.run(debug=True)
