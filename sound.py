import os
import subprocess
import threading


def is_raspberrypi():
    n = os.uname()
    return n[0] == 'Linux' and n[1] == 'raspberrypi'


def _play(fpath):
    subprocess.call('/usr/bin/omxplayer ' + fpath + ' >/dev/null 2>&1', shell=True)


def play(fpath, sync=True):
    if is_raspberrypi() and os.path.exists(fpath):
        if sync:
            _play(fpath)
        else:
            threading.Thread(target=_play, args=(fpath,)).start()


if __name__ == '__main__':
    _play('./sounds/clock_in.mp3')
    _play('./sounds/clock_out.mp3')
