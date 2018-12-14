from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
database = '../clock_in.sqlite3'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db


def all_users():
    cur = get_db().cursor()
    result = cur.execute('select id, name, idm, is_working from users')
    rows = result.fetchall()
    if rows is None:
        return None

    users = []
    for row in rows:
        users.append({'id': row[0], 'name': row[1], 'idm': row[2], 'is_working': str(row[3]) == '1'})
    return users


def find_user(id):
    if not id:
        return None

    cur = get_db().cursor()
    result = cur.execute('select id, name, idm, is_working from users where id = ?', (id,))
    row = result.fetchone()
    if row is None:
        return None

    return {'id': row[0], 'name': row[1], 'idm': row[2], 'is_working': str(row[3]) == '1'}


def update_user(id, name, idm, is_working):
    if not id:
        return None

    cur = get_db().cursor()
    cur.execute('update users set name = ?, idm = ?, is_working = ? where id = ?', (name, idm, is_working, id))
    get_db().commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html', title='All users', users=all_users())


@app.route('/users/<id>/edit')
def edit(id):
    user = find_user(id)
    return render_template('edit.html', title='Edit ' + user['name'], user=find_user(id))


@app.route('/users/<id>', methods=['POST'])
def update(id):
    is_working = '1' if request.form['is_working'] == 'True' else '0'
    update_user(id, name=request.form['name'], idm=request.form['idm'], is_working=is_working)
    return redirect(url_for('edit', id=id))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
