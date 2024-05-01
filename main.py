import http

from flask import Flask, render_template, request, redirect, url_for

from app.html_helper import HtmlHelper
from app.migration_manager import MigrationManager
from app.migrations.migration import Migration
from app.parser_manager import ParserManager
from app.repository import Repository
from settings import RANKS_TABLE_NAME, ROW_COUNT, DESCRIPTIONS_TABLE_NAME

app = Flask(__name__)


@app.route('/ranks', methods=['GET'])
def ranks():
    page = int(request.args.get('page', 0))
    count_ranks = Repository.get_count_rows(RANKS_TABLE_NAME)

    return render_template('ranks.html', data={
        'page': page,
        'buttons': HtmlHelper.get_button_flags(count_ranks, page),
        'ranks': Repository.get_ranks(page)
    })


@app.route('/descriptions', methods=['GET'])
def descriptions():
    page = int(request.args.get('page', 0))
    count_descriptions = Repository.get_count_rows(DESCRIPTIONS_TABLE_NAME)

    return render_template('descriptions.html', data={
        'page': page,
        'buttons': HtmlHelper.get_button_flags(count_descriptions, page),
        'descriptions': Repository
    })


@app.route('/edit/<int:rank_id>', methods=['GET'])
def edit_rank(rank_id: int):
    row = Repository.get_by_id(rank_id, RANKS_TABLE_NAME)
    if len(row) == 0:
        return http.HTTPStatus.NOT_FOUND

    return render_template('edit_rank.html', data={
        'rank': row,
        'taxonomy': Repository.get_taxonomy_names(),
        'samples': Repository.get_samples()
    })


@app.route('/ranks/update', methods=['POST'])
def update_rank():
    taxonomy_id = Repository.get_taxonomy_id_by_name_and_sample_id(
        request.form['taxonomy_name'], int(request.form['sample_id'])
    )
    if len(taxonomy_id) == 0:
        raise Exception('Такой таксономии нет')
    else:
        Repository.update_rank_by_id(
            int(request.form['rank_id']), (request.form['rank_name'], request.form['rank_value'], taxonomy_id[0], )
        )

    return redirect(url_for('ranks'))


@app.route('/delete/<rank_id>', methods=['GET'])
def delete_rank(rank_id: int):
    rank = Repository.get_by_id(rank_id, RANKS_TABLE_NAME)
    if rank is None:
        return http.HTTPStatus.NOT_FOUND

    Repository.delete_by_id(rank_id, RANKS_TABLE_NAME)

    return redirect(url_for('ranks'))


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
