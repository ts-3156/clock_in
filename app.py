#!/usr/bin/env python

import signal
import sys
import time

import db
import slack
import sound
import suica


def signal_handler(signal, frame):
    print('Bye!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def clock_in(idm):
    db.set_working(idm, True)
    return {'idm': idm, 'action': 'clock_in', 'time': time.time()}


def clock_out(idm):
    db.set_working(idm, False)
    return {'idm': idm, 'action': 'clock_out', 'time': time.time()}


if __name__ == '__main__':
    mp3 = {
        'clock_in': './sounds/clock_in.mp3',
        'clock_out': './sounds/clock_out.mp3',
        'too_short_interval': './sounds/too_short_interval.mp3',
        'system_started': './sounds/system_started.mp3',
        'ready_to_touch': './sounds/ready_to_touch.mp3',
    }
    last_action = {'idm': None, 'action': None, 'time': None}

    sound.play(mp3['system_started'])
    sound.play(mp3['ready_to_touch'])

    while True:
        time.sleep(1)
        idm = suica.read()
        if not idm:
            continue

        user = db.find_user(idm)
        if user is None:
            user = db.add_user(idm)

        if idm == last_action['idm'] and time.time() - last_action['time'] < 5:
            sound.play(mp3['too_short_interval'])
            print('too short interval')
            continue

        if user['is_working']:
            last_action = clock_out(idm)
            sound.play(mp3['clock_out'])
            msg = 'Clock out ' + user['name']
            slack.post(msg)
            print(msg)
        else:
            last_action = clock_in(idm)
            sound.play(mp3['clock_in'])
            msg = 'Clock in ' + user['name']
            slack.post(msg)
            print(msg)
