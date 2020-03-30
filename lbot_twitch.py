# lbot_twitch.py

import os
from dotenv import load_dotenv

import requests

from secrets import token_hex
import hmac
import hashlib
import json
import time
import base64

load_dotenv()

try:
    CALLBACK_URL = os.getenv('CALLBACK_URL')
except:
    print('Error: No callback URL found in environment variables!')
    raise EnvironmentError

try:
    TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
except:
    print('Error: No Twitch API Client ID found in environment variables!')
    raise EnvironmentError

try:
    TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
except:
    print('Error: No Twitch API Client secret found in environment variables!')
    raise EnvironmentError

TWITCH_API = 'https://api.twitch.tv/helix'


def get_twitch_token():
    TWITCH_AUTH_URL = 'https://id.twitch.tv/oauth2/token'
    params = {'client_id': TWITCH_CLIENT_ID,
              'client_secret': TWITCH_CLIENT_SECRET, 'grant_type': 'client_credentials'}

    request = requests.post(TWITCH_AUTH_URL, params=params)
    response = request.json()

    print('Twitch API response code: ' + request.status)
    return response


def revoke_twitch_token(token):
    TWITCH_REVOKE_URL = 'https://id.twitch.tv/oauth2/revoke'
    params = {'client_id': TWITCH_CLIENT_ID,
              'token': token}

    request = requests.post(TWITCH_REVOKE_URL, params=params)
    response = request

    print(response)
    return response


def twitch_sub2webhook(mode, topic, lease):
    callback_target = CALLBACK_URL + '/twitchapi/webhooks/callback/'
    TWITCH_WEBHOOK_HUB = TWITCH_API + '/webhooks/hub/'

    # temp_secret = token_hex(nbytes=8)
    # temp_secret = '' # DEBUGGING
    # os.environ['TEMP_SECRET'] = temp_secret # Causes problems on heroku

    try:
        load_dotenv()
        temp_secret = os.environ['TEMP_SECRET']
        # print(temp_secret) # DEBUGGING
    except:
        print('No temporary secret found in environment variables.')
        raise EnvironmentError

    params = {'hub.mode': mode, 'hub.topic': TWITCH_API + topic,
              'hub.callback': callback_target, 'hub.lease_seconds': lease, 'hub.secret': temp_secret}

    header = {'Content-Type': 'application/json',
              'Client-ID': TWITCH_CLIENT_ID}

    request = requests.post(TWITCH_WEBHOOK_HUB, headers=header, params=params)
    response = request

    # print(params, header) # DEBUGGING
    # print(response) # DEBUGGING
    return response
