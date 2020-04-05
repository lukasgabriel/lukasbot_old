# slack.py


import os
from dotenv import load_dotenv

import requests
import json

from lbot_helpers import *


load_dotenv()
try:
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
except:
    print("Error: No Slack Webhook URL found in environment variables!")
    raise EnvironmentError


# send POST request to Slack webhook to post the msg to the Slack channel.
def post(msg):
    webhook_url = SLACK_WEBHOOK_URL
    slack_data = {
        "text": msg,
        "username": "lukasbot-discord",
        "icon_url": "https://github.com/lukasgabriel/lukasbot/blob/master/media/avatar.png",
        "channel": "#lukasbot-discord",
    }

    response = requests.post(
        webhook_url,
        data=json.dumps(slack_data),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        raise APIError(
            response.status_code,
            SLACK_WEBHOOK_URL,
            response.headers,
            response.reason,
            response.text,
        )

    return
