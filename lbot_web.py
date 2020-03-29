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
        print(request.headers['X-Hub-Signature'])
        check = request.data
        check_enc = check.encode('utf-8')
        print(check_enc)

        signature = hmac.new(bytes(123456), bytes(check_enc), hashlib.sha256).hexdigest()
        print(bytes(123456))
        print(bytes(check_enc))

        if hmac.compare_digest(signature, request.headers['X-Hub-Signature'].split('=')[1]):
            print('Signature verified.')

        else:
            print('Signature mismatch!')

        return 'Received.'
        #TODO: Handle incoming notifications.



