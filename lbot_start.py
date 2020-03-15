#               #
# lbot_start.py #
#               #

'''
This module establishes the connection to discord and sets the basic variables.
'''

import time

# for reading the environment variable that contains the discord token
import os
from dotenv import load_dotenv

import requests
import json

from twilio.rest import Client

# Discord Python Library
import discord
from discord.ext import commands

# include command prefix here
comm_prefix = '>'

# sets the command prefix that the bot will respond to
bot = commands.Bot(command_prefix=comm_prefix)

# Sends POST request to Slack webhook to post the msg to the Slack channel.
def slack_post(msg):
    
    webhook_url = 'https://hooks.slack.com/services/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'
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

# Sends SMS via twilio API
def sms_msg(msg, number, author):

    try:
        load_dotenv()
        TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    except:
        print('Error: No Twilio Account SID found in environment variables!')
        raise EnvironmentError

    try:
        load_dotenv()
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
    
# function that does the actual 'starting'
def lbot():
    # load the global variable for the discord token from the env variables
    try:
        load_dotenv()
        DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    except:
        print('Error: No Discord Token found in environment variables!')
        raise EnvironmentError

    # establishes connection with discord API and starts bot locally
    bot.run(DISCORD_TOKEN)

    return
