# discord.py


import time

import os
from dotenv import load_dotenv

import requests

import discord
from discord.ext import commands

import lbot_slack as slack
import lbot_data as data
from lbot_helpers import *


load_dotenv()
try:
    WEBHOOK_ID = os.getenv("WEBHOOK_ID")
    WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN")
except:
    print("Error: No Discord Webhook ID/Token found in environment variables!")
    raise EnvironmentError

try:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
except:
    print("Error: No Discord Token found in environment variables!")
    raise EnvironmentError


# include command prefix here
COMM_PREFIX = ">"

# include channel ID of notification/announcement channel
NOTIFICATION_CHANNEL_ID = 673739313460150287

# include webhook URL for notifications
WEBHOOK_ROOT = "https://discordapp.com/api/webhooks/"

# set the command prefix that the bot will respond to
bot = commands.Bot(command_prefix=COMM_PREFIX)


# establish event that catches the cooldown error and sends it as a message
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = error.retry_after
        cooldown_formatted = time.strftime("%H:%M:%S", time.gmtime(cooldown))
        await ctx.send(
            "This command is on cooldown right now. You can use it again in "
            + cooldown_formatted
            + "."
        )
    raise error


# creates event that prints console output as soon as bot connects to discord
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

    msg = "I've just connected to Discord."

    slack_post(msg)


# sends a single message to a specific channel
async def msg_channel(channel_id, msg):
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(msg)


# sends a message to a discord webhook
def msg_webhok(msg):
    print(msg)  # DEBUGGING
    webhook_target = f"{WEBHOOK_ROOT}{WEBHOOK_ID}/{WEBHOOK_TOKEN}"
    data = {"content": msg}
    response = requests.post(
        webhook_target,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code not in range(200, 299):
        raise APIError(
            response.status_code,
            webhook_target,
            response.headers,
            response.reason,
            response.text,
        )


# function that does the actual 'starting'
def start_bot():
    bot.run(DISCORD_TOKEN)
    return
