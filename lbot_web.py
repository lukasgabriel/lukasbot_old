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
        received_sig = request.headers['X-Hub-Signature']
        # print(received_sig) # DEBUGGING
        # print(request.headers['Content-Length']) # DEBUGGING
        received_json = request.json
        received_bytes = request.data
        print('Notification received. Checking signature...')
        # os.environ['TEMP_SECRET'] = '' # DEBUGGING

        try:
            load_dotenv()
            temp_secret = os.environ['TEMP_SECRET']
            # print(temp_secret) # DEBUGGING
        except:
            print('No temporary secret found in environment variables.')
            temp_secret = ''
            raise EnvironmentError

        expected_hmac = hmac.HMAC(
            bytes(temp_secret, 'utf-8'), received_bytes, 'sha256')
        expected_sig = expected_hmac.digest().hex()
        # print(expected_sig)  # DEBUGGING

        if expected_sig == received_sig.split('=')[1]:
            print('Signature validated.')
        else:
            print('Signature invalid!')
            received_json = None

        os.environ['TEMP_SECRET'] = ''
        return 'Received.'
        # TODO: Handle incoming notifications.
