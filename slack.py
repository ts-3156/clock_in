import os
import requests

URL = 'https://slack.com/api/chat.postMessage'
TOKEN = os.getenv("SLACK_TOKEN", "Not set")
CHANNEL = os.getenv("SLACK_CHANNEL", "Not set")


def post(text):
    res = requests.post(URL, data={'token': TOKEN, 'channel': CHANNEL, 'text': text})
    print(res.text)


if __name__ == '__main__':
    post('This is a post.')
