# lbot_web.py

import os
from dotenv import load_dotenv

import requests

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# TODO: Verify hash of response
@app.route('/twitchapi/webhooks/callback/', methods=['GET', 'POST'])
def twitch_callback():

    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        print('Challenge code received. Returning...')
        return challenge
    else:
        print(request.json)
        print(request.data)
        print(request.form)
        return 'Received.'
        #TODO: Handle incoming notifications.
