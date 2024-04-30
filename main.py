from flask import Flask, render_template

from app.migration_manager import MigrationManager
from app.migrations.migration import Migration
from app.parser_manager import ParserManager
from app.repository import Repository

app = Flask(__name__)


@app.route('/ranks', methods=['GET'])
def ranks():
    return render_template('ranks.html', data=Repository.get_ranks())


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/database/refresh', methods=['POST'])
def refresh_database():
    MigrationManager.refresh()
    return 'База данных успешно пересоздана'


@app.route('/database/migrate', methods=['POST'])
def start_migrate():
    MigrationManager.run_migrations()
    return 'Миграции выполнены успешно'


@app.route('/database/parse', methods=['POST'])
def start_parse():
    parser_manager.start()
    return 'Таблицы заполнены'


if __name__ == '__main__':
    Migration.init()
    Repository.init()
    parser_manager = ParserManager()
    app.run(debug=True)
