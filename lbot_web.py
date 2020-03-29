# lbot_web.py

import requests
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/twitchapi/webhooks/callback/', methods=['GET', 'POST'])
def twitch_callback():
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        print('Challenge is: {0}'.format(challenge))
        return challenge
    else:
        print(request)
        return