#               #
# lbot_start.py #
#               #

'''
This module establishes the connection to discord and sets the basic variables.
'''

# for reading the environment variable that contains the discord token
import os
from dotenv import load_dotenv

# Discord Python Library
import discord
from discord.ext import commands

# include command prefix here
comm_prefix = '>'

# sets the command prefix that the bot will respond to
bot = commands.Bot(command_prefix=comm_prefix)

# creates event that prints console output as soon as bot connects to discord
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

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