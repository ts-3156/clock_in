import os
import subprocess


def is_raspberrypi():
    n = os.uname()
    return n[0] == 'Linux' and n[1] == 'raspberrypi'


def play(fpath):
    if is_raspberrypi() and os.path.exists(fpath):
        subprocess.call('/usr/bin/omxplayer ' + fpath + ' >/dev/null 2>&1', shell=True)


if __name__ == '__main__':
    play('./clock_in.mp3')
    play('./clock_out.mp3')
