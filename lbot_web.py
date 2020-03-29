# lbot_web.py

import os
from dotenv import load_dotenv

import hashlib
import hmac
import json

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
        print(dict(request.headers))
        print(request.json)

        signature = hmac.new(bytes(123456), request.data, hashlib.sha256).hexdigest()

        if hmac.compare_digest(signature, request.headers['X-Hub-Signature'].split('=')[1]):
            print('Signature verified.')

        else:
            print('Signature mismatch!')

        return 'Received.'
        #TODO: Handle incoming notifications.



