#!/usr/bin/env python

import os
import signal
import sqlite3
import subprocess
import sys
import time

import slack
import suica
import name

con = sqlite3.connect('./clock_in.sqlite3')
cur = con.cursor()

clock_in_sound = './clock_in.mp3'
clock_out_sound = './clock_out.mp3'
last_action = {'idm': None, 'action': None, 'time': None}


def signal_handler(signal, frame):
    print('Bye!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def is_raspberrypi():
    n = os.uname()
    return n[0] == 'Linux' and n[1] == 'raspberrypi'


def add_user(idm):
    if idm is None:
        return None

    cur.execute('insert into users (name, idm, is_working) values (?, ?, 1)', (name.gen() + '(Set correct name)', idm))
    con.commit()
    return find_user(idm)


def find_user(idm):
    global cur

    if idm is None:
        return None

    result = cur.execute('select id, name, idm, is_working from users where idm = ?', (idm,))
    row = result.fetchone()
    if row is None:
        return None

    return {'id': row[0], 'name': row[1], 'idm': row[2], 'is_working': str(row[3]) == '1'}


def clock_in(idm):
    global last_action
    cur.execute('update users set is_working = "1" where idm = ?', (idm,))
    con.commit()
    if is_raspberrypi() and os.path.exists(clock_in_sound):
        subprocess.call('/usr/bin/omxplayer ' + clock_in_sound + ' >/dev/null 2>&1', shell=True)
    last_action = {'idm': idm, 'action': 'clock_in', 'time': time.time()}


def clock_out(idm):
    global last_action
    cur.execute('update users set is_working = "0" where idm = ?', (idm,))
    con.commit()
    if is_raspberrypi() and os.path.exists(clock_out_sound):
        subprocess.call('/usr/bin/omxplayer ' + clock_out_sound + ' >/dev/null 2>&1', shell=True)
    last_action = {'idm': idm, 'action': 'clock_out', 'time': time.time()}


if __name__ == '__main__':
    while True:
        time.sleep(1)
        idm = suica.read()
        if idm is None:
            continue

        user = find_user(idm)
        if user is None:
            user = add_user(idm)

        if idm == last_action['idm'] and time.time() - last_action['time'] < 5:
            continue

        if user['is_working']:
            clock_out(idm)
            msg = 'Clock out ' + user['name']
            slack.post(msg)
            print(msg)
        else:
            clock_in(idm)
            msg = 'Clock in ' + user['name']
            slack.post(msg)
            print(msg)
