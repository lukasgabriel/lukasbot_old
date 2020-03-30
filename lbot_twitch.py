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

import lbot_helpers as lh

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

try:
    TWITCH_APP_TOKEN = os.getenv('TWITCH_APP_TOKEN')
except:
    print('Error: No current app token found in environment variables!')
    raise EnvironmentError

TWITCH_API = 'https://api.twitch.tv/helix'


def get_twitch_token():
    TWITCH_AUTH_URL = 'https://id.twitch.tv/oauth2/token'
    params = {'client_id': TWITCH_CLIENT_ID,
              'client_secret': TWITCH_CLIENT_SECRET, 'grant_type': 'client_credentials'}

    try:
        request = requests.post(TWITCH_AUTH_URL, params=params)
        response = request
    except:
        raise lh.APIError(response.status_code, TWITCH_AUTH_URL,
                          response.headers, response.reason, response.text)

    return response


def revoke_twitch_token(token):
    TWITCH_REVOKE_URL = 'https://id.twitch.tv/oauth2/revoke'
    params = {'client_id': TWITCH_CLIENT_ID,
              'token': token}

    try:
        request = requests.post(TWITCH_REVOKE_URL, params=params)
        response = request
    except:
        raise lh.APIError(response.status_code, TWITCH_REVOKE_URL,
                          response.headers, response.reason, response.text)

    print(response)
    return response

# TODO: renew_twitch_token function, storing tokens in file


def get_user_id(name):
    apptoken = TWITCH_APP_TOKEN
    url = TWITCH_API + '/users'

    # Right now, we have to renew the app token by hand every 60 days.
    # TODO: Auto-renewal of app access token.

    try:
        params = {'login': name}
        header = {'Content-Type': 'application/json',
                  'Client-ID': TWITCH_CLIENT_ID, 'Authorization': f'Bearer {apptoken}'}

        request = requests.get(url=url, headers=header, params=params)
        response = request

        # print(response.json) # DEBUGGING
        user_id = response.json()['data'][0]['id']
    except():
        raise lh.APIError(response.status_code, url,
                          response.headers, response.reason, response.text)

    return user_id


def twitch_sub2webhook(mode, topic, lease):
    callback_target = CALLBACK_URL + '/twitchapi/webhooks/callback/'
    TWITCH_WEBHOOK_HUB = TWITCH_API + '/webhooks/hub/'

    # temp_secret = token_hex(nbytes=8)
    # temp_secret = '' # DEBUGGING
    # os.environ['TEMP_SECRET'] = temp_secret # Causes problems on heroku
    # TODO: Store fresh TEMP_KEY in file and hand over to lbot_web.py for signature verification.

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

    # print(params, header)  # DEBUGGING
    # print(response)  # DEBUGGING
    # print(response.reason)  # DEBUGGING
    return response
    # TODO: Handle incoming notifications and forward to discord bot (send msg).
