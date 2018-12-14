import sqlite3

import name

con = sqlite3.connect('/home/pi/Repo/clock_in/clock_in.sqlite3')
cur = con.cursor()


def add_user(idm):
    if not idm:
        return None

    cur.execute('insert into users (name, idm, is_working) values (?, ?, 0)', (name.gen() + '(Set correct name)', idm))
    con.commit()
    return find_user(idm)


def find_user(idm):
    if not idm:
        return None

    result = cur.execute('select id, name, idm, is_working from users where idm = ?', (idm,))
    row = result.fetchone()
    if row is None:
        return None

    return {'id': row[0], 'name': row[1], 'idm': row[2], 'is_working': str(row[3]) == '1'}


def set_working(idm, value):
    cur.execute('update users set is_working = ? where idm = ?', ('1' if value else '0', idm))
    con.commit()


if __name__ == '__main__':
    user = find_user('YOUR_IDM')
    print(user)
