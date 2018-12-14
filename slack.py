import os
import threading
import requests


URL = 'https://slack.com/api/chat.postMessage'
TOKEN = os.getenv("SLACK_TOKEN", "Not set")
CHANNEL = os.getenv("SLACK_CHANNEL", "Not set")


def _post(text):
    res = requests.post(URL, data={'token': TOKEN, 'channel': CHANNEL, 'text': text})
    print(res.text)


def post(text):
    threading.Thread(target=_post, args=(text,)).start()


if __name__ == '__main__':
    post('This is a post.')
