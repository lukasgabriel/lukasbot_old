# lbot_web.py

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/twitchapi/webhooks/callback/', methods=['GET', 'POST'])
def twitch_webhook_callback():
    return 