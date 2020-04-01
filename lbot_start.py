#               #
# lbot_start.py #
#               #

'''
I have to put something in this docstring. #TODO: Add stuff here
'''

import time

import os
from dotenv import load_dotenv

import requests
import json

from twilio.rest import Client

# Discord Python Library
import discord
from discord.ext import commands

import lbot_helpers as lh

load_dotenv()

try:
    WEBHOOK_ID = os.getenv('WEBHOOK_ID')
    WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')
except:
    print('Error: No Discord Webhook ID/Token found in environment variables!')
    raise EnvironmentError

# telephone number address book for sms commands
address_book = {
    'Alex': '+4917621214313',
    'Tommi': '+4915733709805',
    'Lukas': '+491623424473',
    'Gabri': '+4915732612200',
    'Sascha': '+4915733350547',
    'Svenja': '+491725923971',
    'Tolga': '+4915783461039',
    'Gafar': '+4917668547754',
    'Felix': '+4917656761234'
}

# include command prefix here
COMM_PREFIX = '>'

# include channel ID of notification/announcement channel
NOTIFICATION_CHANNEL_ID = 673739313460150287

# include webhook URL for notifications
WEBHOOK_ROOT = 'https://discordapp.com/api/webhooks/'

# set the command prefix that the bot will respond to
bot = commands.Bot(command_prefix=COMM_PREFIX)


# send POST request to Slack webhook to post the msg to the Slack channel.
def slack_post(msg):

    try:
        SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
    except:
        print('Error: No Slack Webhook URL found in environment variables!')
        raise EnvironmentError

    webhook_url = SLACK_WEBHOOK_URL
    slack_data = {
        'text': msg,
        'username': 'lukasbot-discord',
        'icon_url': 'https://github.com/lukasgabriel/lukasbot/blob/master/media/avatar.png',
        'channel': '#lukasbot-discord'
    }

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

    return


# sends a message to a discord webhook
def send2webhook(msg):
    print(msg) # DEBUGGING
    webhook_target = f'{WEBHOOK_ROOT}{WEBHOOK_ID}/{WEBHOOK_TOKEN}'
    response = requests.post(webhook_target, params={'content': msg}, headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise lh.APIError(response.status_code, webhook_target,
                          response.headers, response.reason, response.text)

# get number of recipient from address book
def get_number(recipient):

    recipient_t = recipient.title()

    if recipient_t in address_book:
        number = address_book[recipient_t]
        return number
    else:
        return None


# send SMS via twilio API
def sms_msg(msg, number, author):

    try:
        TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    except:
        print('Error: No Twilio Account SID found in environment variables!')
        raise EnvironmentError

    try:
        TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    except:
        print('Error: No Twilio Auth Token found in environment variables!')
        raise EnvironmentError

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(body=msg,
                                     from_='+12055573240',
                                     to=number)

    slack_post('SMS message sent via twilio with SID: ' + message.sid)

    return


# establish event that catches the cooldown error and sends it as a message
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = error.retry_after
        cooldown_formatted = time.strftime('%H:%M:%S', time.gmtime(cooldown))
        await ctx.send('This command is on cooldown right now. You can use it again in ' + cooldown_formatted + '.')
    raise error


# creates event that prints console output as soon as bot connects to discord
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    msg = 'I\'ve just connected to Discord.'

    slack_post(msg)


# sends a single message to a specific channel
async def send2channel(channel_id, msg):
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(msg)

# function that does the actual 'starting'
def lbot():
    # load the global variable for the discord token from the env variables
    try:
        DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    except:
        print('Error: No Discord Token found in environment variables!')
        raise EnvironmentError

    # establishes connection with discord API and starts bot locally
    bot.run(DISCORD_TOKEN)

    return
