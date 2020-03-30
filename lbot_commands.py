#                  #
# lbot_commands.py #
#                  #

'''
This module contains the custom commands that the bot is able to perform.
'''

import datetime
import random

import lbot_start as start

# Discord Python Library
import discord
from discord.ext import commands

# This API fetches pictures from the GAN sites 'thiscat/persondoesnotexist.com'
from thisapidoesnotexist import get_cat, get_person

# Returns quotes for the cookie command
import fortune

# Module by me that interacts with the Twitch API.
import lbot_twitch as lt

# if unexpected behavior occurs, we don't want to ignore it, but the bot should not stop either
# instead, we just include a print(ERR_RESPONSE) as fallback so we have feedback
err_response = 'BLEEP BLOOP I\'M MALFUNCTIONING PLEASE CALL MY CREATOR @flyomotive TO FIX ME!'

class Error(Exception):
    # Base class for exceptions in this module.
    pass

class InputError(Error):
    # Exception raised for errors in the input.
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

'''
This is where we register each command
'''

# '>hello' - the bot answers to 'hello' with a daytime-specific greeting
@start.bot.command(name='hello', help='You should show some manners and greet the bot. He is our humble servant after all.')
async def hello(ctx):
    
    response = err_response
    author = ctx.message.author.name
    
    greetings_earlymorning = [
        'Good morning, ' + author + '.',
        'Up early, '+ author + '?',
    ]
    greetings_morning = [
        'Good morning,' + author + '.',
        'Hey. Can\'t wait for lunch. What are you having?',
    ]
    greetings_noon = [
        'Nice to see you, ' + author + '.',
        'Hello, ' + author,
    ]
    greetings_afternoon = [
        'Good afternoon, ' + author + '.',
        'Hey, ' + author + '.',
    ]
    greetings_evening = [
        'Good evening, ' + author + '.',
        'Have you had a successful day, ' + author + '?',
    ]
    greetings_night = [
        'Still awake, ' + author + '?',
        'Can\'t sleep, ' + author + '?',
        'Night owl, huh? Me too. \nMatter of fact, I never sleep. Never understood the appeal.',
    ]

    hour = datetime.datetime.now().hour

    if 4 <= hour < 7:
        response = random.choice(greetings_earlymorning)
    elif 8 <= hour < 12:
        response = random.choice(greetings_morning)
    elif 12 <= hour < 15:
        response = random.choice(greetings_noon)
    elif 15 <= hour < 19:
        response = random.choice(greetings_afternoon)
    elif 19 <= hour < 23:
        response = random.choice(greetings_evening)
    else:
        response = random.choice(greetings_night)

    await ctx.send(response)

# '>about' - returns a short description of the bot and its author
@start.bot.command(name='about', help='Lukas made a bot. Tell him how cool that is, right now. Tell him how proud you are.')
async def about(ctx):
    
    response = 'I was made by the glorious @floymotive#1337 to serve him and his friends. He told me he would beat up anyone who is mean to me, so watch out. \n View my source code at https://github.com/lukasgabriel/lukasbot'

    await ctx.send(response)

#'>listcommands' - lists all commands that are currently implemented
@start.bot.command(name='listcommands', help='Lists all commands with a short description of their functionality.')
async def listcommands(ctx):
    
    # TODO: Find a way to return this dict looking nice.
    # cmdlist = {
    #     '>about' : 'I will tell you about myself. This is one of my favorite commands. \n',
    #     '>hello' : 'I will greet you like the gentle-bot I am. \n',
    #     '>listcommands' : 'You just used this. Are you dumb? \n',
    #     '>felixsucks' : 'Self-explanatory. Just stating the obvious. \n',
    #     '>bye' : 'Es ist wie Echos.'
    #     }

    response = 'Currently, I\'m mega stupid and can only tell you how stupid I am. And I can say hello to you if you\'re lonely. When Lukas is done with his exams or gives up on studying, he will make me smarter. So hold tight and have a lot of fun with >about, >listcommands and >hello & >bye!'
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
    goodbottie = [
        'Thank you :)',
        'Aww, thanks.',
        'I\'m just doing my job.',
        'Glad I could help.',
        'Don\'t mention it.',
        'I\'m here to help.',
        ':)',
        '(っ◕‿◕)っ',
        '( ˘ ³˘)♥',
        'Thank you so much.',
        'Thanks, I appreciate it.',
        'Thank you!'
        ]

    response = random.choice(goodbottie)

    await ctx.send(response)

# '>bye' - the bot can tell you good-bye
@start.bot.command(name='bye', help='Es ist wie Spiegel.')
async def bye(ctx):

    author = ctx.message.author.name
    response = 'Good-bye, ' + author + '.'

    goodbyes = [
        'Good-bye, ' + author + '.',
        'Farewell, ' + author + '.',
        'See you soon, ' + author + '.',
        'Stay safe, ' + author + '.',
        'Stay safe, ' + author + '.',
        'See you later, alligator!',
        'Take care, ' + author + '.',
        'Tschau mit V'
    ]

    response = random.choice(goodbyes)

    await ctx.send(response)

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

# '>calc' - a calculator, because people requested that
#@start.bot.command(name='calc', help='A calculator. Use x+y and x-y for addition and subtraction; x*y and x/y for multiplication and division; x**n for x to the power of n and ''n r x'' for the nth root of x; x//y for floor division and %\x for the modulo operation; x! for x factorial and ''x o n'' for x over n (binomial coefficient); ''x gcd y'' returns the greatest common divisor of x and y.')
#async def calc(ctx):
#    
#    person = get_person()
#
#    person.save_image('media\\temp\person.jpeg')
#
#    await ctx.send(file=discord.File('media\\temp\person.jpeg'))
#
# TODO: Idea with calculator: support other operations as well, all kinds of cool math and visualisation stuff
# like creating a diagram for a specified function oder something like that

# '>whattoplay' - Gives a suggestion what the gang gang could play together.
@start.bot.command(name='whattoplay', help='I\'ll give you a suggestion what you could play together')
async def whattoplay(ctx):

    mp_games = [
        'Gang Beasts',
        'Age of Empires: Definitive Edition',
        'RAFT',
        'Monster Hunter: World',
        'League of Legends',
        'Rocket League',
        'Gwent',
        'Terraria...with Mods',
        'Escape from Tarkov',
        'Temtem',
        'Wolcen: Lords of Mayhem',
        'skribbl.io',
        'UNO',
        'Cards Against Humanity',
        'nothing, and go outside instead',
        'nothing, ands study instead',
        'Halo: Master Chief Collection',
        'Tower Unite',
        'Tabletop Simulator',
        'Garry\'s Mod',
        'Deep Rock Galactic',
        'Counter-Strike: Global Offensive',
        'DotA 2',
        'Starbound',
        'MORDHAU',
        'ASTRONEER',
        'Destiny 2',
        'Modded Minecraft',
        'Warframe',
        'Unturned',
        'Left 4 Dead 2',
        'Portal 2 Co-Op',
        'Apex Legends',
        'Fortnite',
        'Spellsworn',
        'SCUM',
        'Read Dead Redemption 2',
        'ShellShock Live',
        'Grand Theft Auto V',
        'Darwin Project',
        'BattleBlock Theater',
        'SpeedRunners',
        'OverCooked 2',
        'Plants vs Zombies: Battle for Neighborville',
        'Borderlands 3',
        'Sea of Thieves',
        'Divinity: Original Sin',
        'Overwatch',
        'Keep Talking and Nobody Explodes',
        'Payday',
        'Payday 2',
        'Rainbow Six: Siege',
        'TowerFall Ascension',
        'Jackbox Party Game Series',
        'Nidhogg',
        'Octodad',
        'Ultimate Chicken Horse',
        'Screencheat',
        'Call of Duty: Modern Warfare',
        'Trouble in Terrorist Town',
        'Mario Kart 8',
        'Mario Party',
        'Garry\'s Mod: Murder',
        'PUBG',
        'Super Smash Bros. Ultimate',
        'Team Fortress 2',
        'Don\'t Starve Together',
        'Monday Night Combat',
        'Battlefield 2',
        'Star Wars: Battlefront (Classic)',
        'GTA: San Andreas Multiplayer',
        'Old School RuneScape',
        'A Way Out',
        'Half Life: Deathmatch',
        'TES V: Skyrim - Multiplayer Mod',
        'The Forest',
        'ARK: Survival Evolved',
        'Rust',
        'Life is Feudal',
        'Roblox',
        'Habbo Hotel',
        'GeoGuessr',
        'MS Paint Adventures',
        'Town of Salem',
        'Fallout 76   .....just kidding lmao, don\'t fucking touch that game with a 100 ft pole'            
    ]

    response = 'Hmmm, let me think...  today, you could play ' + random.choice(mp_games) + '!'

    await ctx.send(response)

# '>addgame' - add a game to the list that 'whattoplay' uses (currently have to be added manually)
@start.bot.command(name='addgame', help='Add a game to the list of games that I suggest when you call ''>whattoplay''')
async def addgame(ctx):

    author = ctx.message.author.name
    game_wish = ctx.message.content[9:]
    record = author + ' suggested the game ' + game_wish + ' via the \'>addgame\' command.'

    start.slack_post(record)
    
    msgresponse = author + ', you added \'' + game_wish + '\' to the list. Thank you for your suggestion!'

    await ctx.send(msgresponse)

# '>addresses' - read recipients (keys) from address_book dict
@start.bot.command(name='addresses', help='Returns all address book entries that currently have their phone number set and can receive SMS messages.')
async def addresses(ctx):

    recipients = ''

    for key in start.address_book:
        recipients += '  -  ' + key 

    await ctx.send('The following recipients are available:' + recipients)

# '>sms' - send sms via twilio
@start.bot.command(name='sms', help='Send an SMS. Format your request like so:  MESSAGE : RECIPIENT  -  you can view the command\'s address book with the \'>addresses\' command.')
@commands.cooldown(2, 7200, commands.BucketType.guild) # Command can be used two times per 120 minutes before triggering a server-wide cooldown of 2 hours.
async def sms(ctx):

    # TODO: Create webhook to receive and forward replies to discord channels.
    # TODO: Implement tracking of SMS delivery status via webhook.
    # TODO: Create reminder functionality to let users set SMS reminders for themselves.

    try:
        author = ctx.message.author.name
        msg_raw = ctx.message.content[4:]

        msg = 'Message from ' + author + ': ' + msg_raw.rsplit(':', 1)[0].strip()
        recipient_raw = msg_raw.rsplit(':', 1)[1]
        recipient = recipient_raw.strip()
        number = start.get_number(recipient)

        if number != None:
            start.sms_msg(msg, number, author)
            start.slack_post('SMS request received from ' + author + ' to ' + recipient + ' with message: ' + msg_raw.rsplit(':', 1)[0])
            msgresponse = 'Outbound SMS request received.'
        else:
            msgresponse = 'Recipient not found in address book. Check your spelling or have a look at the address book with \'>addresses\'.'

    except:
        msgresponse = 'Invalid message format. Use \'>help sms\' for more info.'

    await ctx.send(msgresponse)

# '>twitch_notify' - establishes notification for stream events (went live, went offline) for specified channel.
@start.bot.command(name='twitch_notify', help='Currently WIP. Format your command like so: STREAMER_NAME : [on/off]')
@commands.cooldown(2, 86500, commands.BucketType.guild) # Command can be used twice per day before triggering a 24-hour cooldown.
async def twitch_notify(ctx):
    command_raw = ctx.message.content[15:]

    try:
        streamer = command_raw.split(':', 1)[0].strip()
        mode_raw = command_raw.rsplit(':', 1)[1].strip()

        if 'on' in mode_raw:
            mode = 'subscribe'
        elif 'off' in mode_raw:
            mode = 'unsubscribe'
        else:
            raise InputError

        lease =  865000 # Might add auto-renewal feature; for now, we'll use the Twitch API maximum of 10 days.
        duration = '{:0>8}'.format(str(datetime.timedelta(seconds=lease)))
        
        topic = lt.TWITCH_API + '/streams?user_login=' + streamer # Could be changed to notify of other events.

        response = lt.twitch_sub2webhook(mode, topic, lease)

        if response.status_code == lt.requests.codes.ok:
            msgresponse = f'You\'ve successfully enabled notifcations to channel updates from {streamer} for {duration}.' 
        else:
            msgresponse = 'Something went wrong.'

    except(ValueError):
        msgresponse = 'Invalid command format. Use \'>help twitch_notify\' for more info.'
        
    await ctx.send(msgresponse)

