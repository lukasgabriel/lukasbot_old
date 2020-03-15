#                  #
# lbot_commands.py #
#                  #

'''
This module contains the custom commands that the bot is able to perform.
'''

import datetime
import random

import requests
import json

import lbot_start as start

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
    
    response = 'I was made by the glorious @floymotive#1337 to serve him and his friends. He told me he would beat up anyone who is mean to me, so watch out.'

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
        'Fallout 76   .....just kiiding lmao, don\'t fucking touch that game with a 100 ft pole'            
    ]

    response = 'Hmmm, let me think...  today, you could play ' + random.choice(mp_games) + '!'

    await ctx.send(response)

# '>addgame' - add a game to the list that 'whattoplay' uses (currently have to be added manually)
@start.bot.command(name='addgame', help='Add a game to the list of games that I suggest when you call ''>whattoplay''')
async def addgame(ctx):

    author = ctx.message.author.name
    game_wish = ctx.message.content[9:]
    record = author + ' suggested the game ' + game_wish + ' via the \'>addgame\' command.'

    webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = {
                 'text': record,
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

    msgresponse = author + ', you added \'' + game_wish + '\' to the list. Thank you for your suggestion!'

    await ctx.send(msgresponse)

# '>kms' - kills yourself
@start.bot.command(name='kms', help='Allows you to kill yourself.')
async def kms(ctx):

    author = ctx.message.author.name

    response = author + ' has killed themselves.'

    suicides = [
        author + ' shot themselves in the head.',
        'Cleanup in aisle 5, \'cause ' + author + ' blasted their brains out.',
        author + 'just hung themselves. :PepeHang:',
        author + ' jumped into an industrial hydraulic press, and is now dead.',
        author + ' took 25 sleeping pills and ended it all.',
        'Oh no! Someone found you in time and called an ambulance, you are now alive but crippled for life.',
        author + ' jumped out of a 25th story window and went splat.',
        author + ' jumped in front of a train, killing themselves and traumatizing the driver for life.',
        author + ' tied their foot to a heavy rock and kicked it down a waterfall. They are now fish food.',
        author + ' covered themselves in gasoline, set it on fire and burned to a crisp.',
        author + ' wanted one last crazy trip and gave themselves the golden shot.',
        author + ' overdosed on pain meds and choked on their own vomit.',
        author + ' drank two litres of bleach and died a very painful death.',
        author + ' closed the garage door and left the engine running until they passed out.',
        author + ' chose honor over life and committed seppuku. They are now a human kebab.',
        author + ' built a bomb at home and went out with a bang.',
        author + ' jumped in front of a chool bus. 37 school children will never laugh again.',
        author + ' jumped out of an airplane ... without a parachute.',
        author + ' cut their radial artery in the bathtub and bled to death.'
    ]

    response = random.choice(suicides)

    await ctx.send(response)

# '>cookie' - reads a fortune cookie quote to the user
#@start.bot.command(name='cookie', help='Reads a fortune cookie quote to you.')
#async def cookie(ctx):
#
#    try:
#        start.load_dotenv()
#        FORTUNE_FILE = start.os.getenv('FORTUNE_FILE')
#    except:
#        print('Error: No Fortune file path specified in environment variables!')
#        raise EnvironmentError
#
#    response = exec(fortune)
#
#    await ctx.send(response)
