# lbot_web.py


import os
from dotenv import load_dotenv

import hashlib
import hmac

import requests
import json

from flask import Flask
from flask import request

import lbot_discord as discord
import lbot_twitch as lt


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


# TODO: Verify hash of response
@app.route("/twitchapi/webhooks/callback/", methods=["GET", "POST"])
def twitch_callback():

    if request.method == "GET":
        challenge = request.args.get("hub.challenge")
        print("Challenge code received. Returning...")
        return challenge

    # TODO: Move signature verification to its own function.
    else:
        received_sig = request.headers["X-Hub-Signature"]
        # print(received_sig) # DEBUGGING
        # print(request.headers['Content-Length']) # DEBUGGING
        received_json = request.json
        received_bytes = request.data
        print("Notification received. Checking signature...")
        # os.environ['TEMP_SECRET'] = '' # DEBUGGING

        try:
            load_dotenv()
            temp_secret = os.environ["TEMP_SECRET"]
            # TODO: Reading TEMP_KEY from file so it gets generated and handed over by lbot_twitch.py
            # print(temp_secret) # DEBUGGING
        except:
            print("No temporary secret found in environment variables.")
            temp_secret = ""
            raise EnvironmentError

        expected_hmac = hmac.HMAC(bytes(temp_secret, "utf-8"), received_bytes, "sha256")
        expected_sig = expected_hmac.digest().hex()
        # print(expected_sig)  # DEBUGGING

        if expected_sig == received_sig.split("=")[1]:
            print("Signature validated.")
            # print(received_json) # DEBUGGING

            if len(received_json["data"]) > 0:
                streamer_name = received_json["data"][0]["user_name"]
                stream_game = lt.get_game_name(received_json["data"][0]["game_id"])
                stream_title = received_json["data"][0]["title"]

                print(
                    "Received notification for stream change event. Sending message..."
                )
                notification_msg = f"{streamer_name} is now streaming {stream_game}  -  {stream_title}  ->  https://twitch.tv/{streamer_name}"
                # start.send2channel(start.NOTIFICATION_CHANNEL_ID, notification_msg) # Does not work
                discord.msg_webhook(notification_msg)
            else:
                print("Received notification for stream offline event. Ignoring...")

        else:
            print("Signature invalid! Ignoring...")
            received_json = None

        return "Received."
        # TODO: Handle incoming notifications.
