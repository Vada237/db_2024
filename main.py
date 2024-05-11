import http

from flask import Flask, render_template, request, redirect, url_for

from app.html_helper import HtmlHelper
from app.migration_manager import MigrationManager
from app.migrations.migration import Migration
from app.parser_manager import ParserManager
from app.repository import Repository
from settings import RANKS_TABLE_NAME, DESCRIPTIONS_TABLE_NAME

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
        'descriptions': Repository.get_descriptions(page)
    })


@app.route('/add_description', methods=['GET'])
def add_description():
    return render_template('create_description.html', data={
        'samples': Repository.get_samples()
    })


@app.route('/descriptions/create', methods=['POST'])
def create_description():
    Repository.create_description(
        (
            int(request.form['sample_id']),
            request.form['location'],
            request.form['coordinates_x'],
            request.form['coordinates_y'],
            HtmlHelper.str_null_to_none(request.form['soil_type']),
            HtmlHelper.numbers_to_float(request.form['elevation']),
            HtmlHelper.numbers_to_float(request.form['depth']),
            request.form['body_site'],
            HtmlHelper.numbers_to_float(request.form['temperature']),
            HtmlHelper.numbers_to_float(request.form['ph'])
        )
    )

    return redirect(url_for('descriptions'))


@app.route('/edit_description/<int:description_id>', methods=['GET'])
def edit_description(description_id: int):
    row = Repository.get_by_id(description_id, DESCRIPTIONS_TABLE_NAME)
    if len(row) == 0:
        return http.HTTPStatus.NOT_FOUND

    return render_template('edit_description.html', data={
        'description': row,
        'samples': Repository.get_samples()
    })


@app.route('/delete_description/<int:description_id>', methods=['GET'])
def delete_description(description_id: int):
    row = Repository.get_by_id(description_id, DESCRIPTIONS_TABLE_NAME)
    if len(row) == 0:
        return http.HTTPStatus.NOT_FOUND

    Repository.delete_by_id(description_id, DESCRIPTIONS_TABLE_NAME)

    return redirect(url_for('descriptions'))


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


@app.route('/ranks/add', methods=['GET'])
def add_ranks():
    return render_template('create_rank.html', data={
        'taxonomy': Repository.get_taxonomy_names(),
        'samples': Repository.get_samples()
    })


@app.route('/ranks/create', methods=['POST'])
def create_ranks():
    taxonomy_id = Repository.get_taxonomy_id_by_name_and_sample_id(
        request.form['taxonomy_name'], int(request.form['sample_id'])
    )
    if len(taxonomy_id) == 0:
        raise Exception('Такой таксономии нет')
    else:
        Repository.create_rank((
            taxonomy_id[0],
            request.form['_kingdom'],
            request.form['_phylum'],
            request.form['_class'],
            request.form['_order'],
            request.form['_family'],
            request.form['_genus']
        ))

    return redirect(url_for('ranks'))


@app.route('/ranks/update', methods=['POST'])
def update_rank():
    taxonomy_id = Repository.get_taxonomy_id_by_name_and_sample_id(
        request.form['taxonomy_name'], int(request.form['sample_id'])
    )
    if len(taxonomy_id) == 0:
        raise Exception('Такой таксономии нет')
    else:
        Repository.update_rank_by_id(
            int(request.form['rank_id']), (
                taxonomy_id[0],
                request.form['_kingdom'],
                request.form['_phylum'],
                request.form['_class'],
                request.form['_order'],
                request.form['_family'],
                request.form['_genus']
            )
        )

    return redirect(url_for('ranks'))


@app.route('/descriptions/update', methods=['POST'])
def update_descriptions():
    if 'sample_id' not in request.form:
        return 'Вы не выбрали образец, вернитесь обратно и выберите образец'

    Repository.update_description_by_id(int(request.form['description_id']), [
        int(request.form['sample_id']),
        request.form['location'],
        request.form['coordinates_x'],
        request.form['coordinates_y'],
        HtmlHelper.str_null_to_none(request.form['soil_type']),
        HtmlHelper.numbers_to_float(request.form['elevation']),
        HtmlHelper.numbers_to_float(request.form['depth']),
        request.form['body_site'],
        HtmlHelper.numbers_to_float(request.form['temperature']),
        HtmlHelper.numbers_to_float(request.form['ph'])
    ])

    return redirect(url_for('descriptions'))


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
