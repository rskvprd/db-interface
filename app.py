from flask import Flask, render_template, request, flash, g
from FIELD_TYPE import FIELD_TYPES
from authorisation import authorisation, login_manager
from secrets import token_hex
from flaskext.mysql import MySQL


def create_app():
    # Initialise application
    app = Flask(__name__)
    # Database configuration
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'wasya2001'
    app.config['MYSQL_DATABASE_DB'] = 'curds'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    # Login configuration
    login_manager.init_app(app)
    secret_key = token_hex()
    app.secret_key = secret_key
    # Register blueprints
    app.register_blueprint(authorisation, url_prefix='/authorisation')
    return app


app = create_app()


def get_cursor(mysql_object):
    if 'cur' not in g:
        g.cur = get_db(mysql_object).cursor()
    return g.cur


def get_db(mysql_object):
    if 'db' not in g:
        g.db = mysql_object.connect()
    return g.db


def readable_description(description):
    description = [list(a) for a in description]
    for column_header in description:
        field_id = column_header[1]
        column_header[1] = FIELD_TYPES[field_id]
    return description


def get_table_data(table_name):
    cur = get_cursor(g.sql)
    cur.execute(f'SELECT * FROM {table_name}')
    desc = readable_description(cur.description)

    return {
        'name': table_name,
        'rows': cur.fetchall(),
        'description': desc
    }


@app.route('/')
def index():
    flash('abobus')
    return render_template('index.html')


@app.route('/admin/add', methods=['POST'])
def add_table():
    cur = get_cursor(g.sql)
    try:
        cur.execute(f'CREATE TABLE {request.data.decode()};')
        return 'ok'
    except Exception as e:
        return str(e)


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    cur = get_cursor()
    if request.method == 'GET':
        cur.execute('SHOW TABLES;')
        tables = cur.fetchall()
        data = get_table_data(tables[0][0])

        return render_template('admin.html', tables=tables, data=data)
    if request.method == 'POST':
        if request.is_json:
            current_table = request.get_json()['table']
        else:
            current_table = request.get_data(as_text=True)
        try:
            data = get_table_data(current_table)
        except Exception as e:
            data = {'error': e}
        return render_template('db-table__content.html', data=data)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
