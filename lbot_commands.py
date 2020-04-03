#                  #
# lbot_commands.py #
#                  #

'''
This module contains the custom commands that the bot is able to perform.
'''
# Time and timezones
import datetime
import pytz

# Random numbers (not for security)
import random

# Module by me that interacts with the Twitch API.
import lbot_twitch as lt

# Module by me that initializes the bot and contains variables.
import lbot_start as start

# Module by me that contains some additional stuff but is used by other modules as well.
import lbot_helpers as lh

# Module that contains shared functions. TODO: Move all non-discord-specific functions here!
import lbot_functions as lf

# Module that contains the long text strings/lists used in some of the commands so this file with the actual code doesn't become so long.
import lbot_data as ld

# Discord Python Library
import discord
from discord.ext import commands

# This API fetches pictures from the GAN sites 'thiscat/persondoesnotexist.com'
from thisapidoesnotexist import get_cat, get_person

# Returns quotes for the cookie command
import fortune


# if unexpected behavior occurs, we don't want to ignore it, but the bot should not stop either
# instead, we just include a print(ERR_RESPONSE) as fallback so we have feedback
err_response = 'BLEEP BLOOP I\'M MALFUNCTIONING PLEASE CALL MY CREATOR @flyomotive TO FIX ME!'


'''
This is where we register each command
'''


# '>hello' - the bot answers to 'hello' with a daytime-specific greeting
@start.bot.command(name='hello', help='You should show some manners and greet the bot. He is our humble servant after all.')
async def hello(ctx):
    response = err_response
    author = ctx.message.author.name

    # Get UTC first, then local time, then the 'hour' component.
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    germany_now = utc_now.astimezone(pytz.timezone('Europe/Berlin'))
    hour = germany_now.hour

    if 4 <= hour < 7:
        response = random.choice(ld.greetings_earlymorning)
    elif 8 <= hour < 12:
        response = random.choice(ld.greetings_morning)
    elif 12 <= hour < 15:
        response = random.choice(ld.greetings_noon)
    elif 15 <= hour < 19:
        response = random.choice(ld.greetings_afternoon)
    elif 19 <= hour < 23:
        response = random.choice(ld.greetings_evening)
    else:
        response = random.choice(ld.greetings_night)

    await ctx.send(response.format(author))


# '>about' - returns a short description of the bot and its author
@start.bot.command(name='about', help='Lukas made a bot. Tell him how cool that is, right now. Tell him how proud you are.')
async def about(ctx):
    response = ld.about

    await ctx.send(response)


# '>vibecheck' - currently, you can't fail the vibe check.
@start.bot.command(name='vibecheck', help='VIBE CHECK')
async def vibecheck(ctx):
    # TODO: make it so users can fail the vibe check.
    response = 'Passed.'

    await ctx.send(response)


# '>goodbot' - users can compliment the bot and it will answer with one grateful message from the list
@start.bot.command(name='goodbot', help=':)')
async def goodbot(ctx):
    # TODO: add a 'badbot' command with a field for 'reason' and corresponding 'score' for the bot for feedback
    response = random.choice(ld.goodbottie)

    await ctx.send(response)


# '>bye' - the bot can tell you good-bye
@start.bot.command(name='bye', help='Es ist wie Spiegel.')
async def bye(ctx):
    author = ctx.message.author.name
    response = random.choice(ld.goodbyes)

    await ctx.send(response.format(author))


# '>cat' - pulls a generated cat picture via 'thisapidoesnotexist', saves it temporarily and sends it to the context
@start.bot.command(name='cat', help='Shows you a picture of a cat that doesn\'t exist. A fictious feline.')
async def cat(ctx):
    cat = get_cat()

    cat.save_image('media\\temp\cat.jpeg')

    await ctx.send(file=discord.File('media\\temp\cat.jpeg'))


# '>person' - pulls a generated 'person' picture via 'thisapidoesnotexist', saves it temporarily and sends it to the context
@start.bot.command(name='person', help='Shows you a picture of a person that doesn\'t exist.')
async def person(ctx):
    person = get_person()

    person.save_image('media\\temp\person.jpeg')

    await ctx.send(file=discord.File('media\\temp\person.jpeg'))


# '>whattoplay' - Gives a suggestion what the gang gang could play together.
@start.bot.command(name='whattoplay', help='I\'ll give you a suggestion what you could play together')
async def whattoplay(ctx):
    response = 'Hmmm, let me think...  today, you could play ' + \
        random.choice(ld.mp_games) + '!'

    await ctx.send(response)


# '>addgame' - add a game to the list that 'whattoplay' uses (currently have to be added manually)
@start.bot.command(name='addgame', help='Add a game to the list of games that I suggest when you call ''>whattoplay''')
async def addgame(ctx):
    author = ctx.message.author.name
    game_wish = ctx.message.content[9:]
    record = author + ' suggested the game ' + \
        game_wish + ' via the \'>addgame\' command.'

    start.slack_post(record)

    msgresponse = author + ', you added \'' + game_wish + \
        '\' to the list. Thank you for your suggestion!'

    await ctx.send(msgresponse)


# '>addresses' - read recipients (keys) from address_book dict
@start.bot.command(name='addresses', help='Returns all address book entries that currently have their phone number set and can receive SMS messages.')
async def addresses(ctx):
    recipients = ''
    for key in ld.address_book:
        recipients += '  -  ' + key

    await ctx.send('The following recipients are available:' + recipients)


# '>sms' - send sms via twilio
@start.bot.command(name='sms', help='Send an SMS. Format your request like so:  MESSAGE : RECIPIENT  -  you can view the command\'s address book with the \'>addresses\' command.')
# Command can be used two times per 120 minutes before triggering a server-wide cooldown of 2 hours.
@commands.cooldown(2, 7200, commands.BucketType.guild)
async def sms(ctx):
    # TODO: Create webhook to receive and forward replies to discord channels.
    # TODO: Implement tracking of SMS delivery status via webhook.
    # TODO: Create reminder functionality to let users set SMS reminders for themselves.

    try:
        author = ctx.message.author.name
        msg_raw = ctx.message.content[4:]

        msg = 'Message from {author}: ' + \
            msg_raw.rsplit(':', 1)[0].strip()
        recipient_raw = msg_raw.rsplit(':', 1)[1]
        recipient = recipient_raw.strip()
        number = start.get_number(recipient)

        if number != None:
            start.sms_msg(msg, number, author)
            start.slack_post('SMS request received from {author} to ' +
                             recipient + ' with message: ' + msg_raw.rsplit(':', 1)[0])
            msgresponse = 'Outbound SMS request received.'
        else:
            msgresponse = 'Recipient not found in address book. Check your spelling or have a look at the address book with \'>addresses\'.'

    except:
        msgresponse = 'Invalid message format. Use \'>help sms\' for more info.'

    await ctx.send(msgresponse)


# '>twitch_notify' - establishes notification for stream events (went live, went offline) for specified channel.
@start.bot.command(name='twitch_notify', help='Currently WIP. Format your command like so: STREAMER_NAME : [on/off]')
# Command can be used twice per day before triggering a 24-hour cooldown.
@commands.cooldown(4, 86400, commands.BucketType.guild)
async def twitch_notify(ctx):
    command_raw = ctx.message.content[15:]
    author = ctx.message.author.name

    try:
        streamer_name = command_raw.split(':', 1)[0].strip()
        mode_raw = command_raw.rsplit(':', 1)[1].strip()

        if 'on' in mode_raw:
            mode = 'subscribe'
            mode_state = 'enabled'
        elif 'off' in mode_raw:
            mode = 'unsubscribe'
            mode_state = 'disabled'
        else:
            raise lh.InputError(
                message='Invalid command format. Use \'>help twitch_notify\' for more info.')

        # TODO: Add auto-renewal feature; for now, we'll use the Twitch API maximum of 10 days.
        lease = 864000
        duration = '{:0>8}'.format(str(datetime.timedelta(seconds=lease)))

        streamer_id = lt.get_user_id(streamer_name)

        # Could be changed to notify of other events.
        topic = '/streams?user_id=' + streamer_id

        response = lt.twitch_sub2webhook(mode, topic, lease)

        if response.status_code == 202:
            if mode_state == 'enabled':
                msgresponse = f'You\'ve successfully {mode_state} notifications to channel updates from {streamer_name} for {duration}.'
                start.slack_post(
                    f'{author} {mode_state} notifications to channel updates from {streamer_name} for {duration}.')
            if mode_state == 'disabled':
                msgresponse = f'You\'ve successfully {mode_state} notifications to channel updates from {streamer_name}.'
                start.slack_post(
                    f'{author} {mode_state} notifications to channel updates from {streamer_name}.')
        else:
            raise lh.APIError(code=response.status_code, url=topic,
                              headers=response.headers, msg=response.reason, text=response.text)

    except lh.APIError as err:
        msgresponse = f'Something went wrong. Error {err.code} - {err.msg}'
    except lh.InputError as err:
        msgresponse = f'Input Error: {err.message}'
    except(TypeError, KeyError, ValueError, SyntaxError, IndexError):
        msgresponse = 'Invalid command format. Use \'>help twitch_notify\' for more info.'
    except():
        msgresponse = 'Unspecified error. @bot_dad'

    await ctx.send(msgresponse)


# '>magic8ball' - users can shake the 'magic 8-ball' and get a random answer.
@start.bot.command(name='magic8ball', help='Ask the magic 8-ball for its infinite wisdom.')
async def magic8ball(ctx):
    response = random.choice(ld.magic_8ball)
    await ctx.send(response)


# '>dice' - users can roll a dice with as many sides as they want
@start.bot.command(name='dice', help='Roll a dice. You can choose how many sides the dice should have (default is 6).')
async def dice(ctx):
    command_raw = ctx.message.content[6:]
    author = ctx.message.author.name

    try:
        sides = int(command_raw)
        if sides < 1_000_000_000_000_000:
            roll = random.randint(1, sides)
            response = f'{author} rolled a {roll} out of {sides}.'
        else:
            response = 'That number is a little large, my dude. Compensating for something?'
    except ValueError:
        response = 'Invalid command format. Use \'>help dice\' for more info.'

    await ctx.send(response)


# '>urban' - returns the urban dictionary definition for the user-specified search term - powered by UrbanScraper (http://urbanscraper.herokuapp.com/).
@start.bot.command(name='urban', help='You can look up the urban dictionary definition for a word using this command.')
# Command can be used five times per minute before triggering a 5-minute cooldown.
@commands.cooldown(5, 300, commands.BucketType.guild)
async def urban(ctx):
    command_raw = ctx.message.content[6:]
    term = command_raw.strip()
    response = lf.get_urban_definition(term)

    try:

        if response != False:
            term = response[0]
            definition = response[1]
            url = response[2]
            example = response[3]
            msgresponse = f'I found the following definition for \'{term}\' on urbandictionary.com: \n -> \"{definition}\" \n \n -> Example: {example} \n -> Link to definition: {url}'

        else:
            msgresponse = 'Sorry, but I couldn\'t find a definition for {term} on urbandictionary.com'

    except Exception as e:
        msgresponse = 'An error occured.'
        raise e

    await ctx.send(msgresponse)
