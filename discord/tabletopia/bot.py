import os
import random
import json
import discord
from dotenv import load_dotenv
from discord import ChannelType
from discord.ext import commands
load_dotenv()

HOME = os.getenv("DISCORD_BOT_HOME") + '/tabletopiaHelper'


with open(HOME + '/auth.json') as f:
    TOKEN = json.loads(f.read())['token']

with open(HOME + '/package.json') as f:
    PACKAGE = json.loads(f.read())

bot = commands.Bot(command_prefix='\\', intents=discord.Intents(messages=True, guilds=True, members=True))

# TODO:
# command to look up tabletopia rules for last tabletopia room game
# command to find a how to play youtube video for last tabletopia room game
# command to pick random game that plays up to 5 by default
# perhaps after getting the games look up ratings for the games.

# look at history in the form of a list
# messages = await channel.history().flatten()
# for message in messages:
#     print(message)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')
    # TODO: pick new icon for avatar
    # HOME + '/avatars'


@bot.event
async def on_message(message):
    if message.content == "hello":
        await message.channel.send('Hello to you')

    await bot.process_commands(message)


@bot.command(name='quote', help='Responds with a random board game quote', brief='Board game quote')
async def random_quote(ctx):
    board_game_quotes = [
        '"Bomb it, pave it, make a parking lot out of it!" -- Anon.',
        '"The meek shall inherit the earth. The rest of us are going to the stars!" -- Anon.',
        '"Nuke em till they glow, and shoot em in the dark!" -- Anon.',
        '"Cards are war, in disguise of a sport." -- Charles Lamb',
        '"Lose your first 50 games as quickly as possible." -- Go proverb',
        '"If you\'re not prepared to lose every friend you have over a board game, you\'re not playing hard enough." '
        '-- Anon.',
        '"Never bored with a board game" -- Anon.',
    ]

    response = random.choice(board_game_quotes)
    await ctx.send(response)


@bot.command(name='random', help='Responds with a random number between 0 and 100', brief='Random number')
async def random_number(ctx):
    response = random.randrange(0, 100)
    await ctx.send(response)


@bot.command(
    name='random_player', help='Responds with a random player in the general text chat', brief='Random player',
    aliases=['rp', 'fp', 'pick', 'first_player', 'firstplayer', 'randomplayer']
)
async def random_player(ctx):
    members = []
    for member in discord.utils.get(ctx.guild.channels, name="general", type=ChannelType.text).members:
        print(f'member: {member.name}, status: {member.status}, bot: {member.bot}')
        # if not member.bot and member.status == Status.online:
        if not member.bot:
            members.append(member.name)

    if len(members) < 1:
        members.append('Nobody in channel?')

    response = random.choice(members)
    await ctx.send(response)


@bot.command(name='clear', help='Clear request and response to commands', brief='Clear command messages')
async def clear_messages(ctx):
    def is_me(m):
        return m.author == bot.user

    def is_command(m):
        if m.content:
            return m.content[0] == '\\'
        else:
            return False

    bot_deleted = await ctx.channel.purge(limit=100, check=is_me)
    deleted = await ctx.channel.purge(limit=100, check=is_command)
    await ctx.channel.send('Deleted {} message(s)'.format(len(bot_deleted) + len(deleted)))


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command(name='test', help='Used to test whatever I am currently working on', brief='test')
async def test_command(ctx):
    members = []
    for member in discord.utils.get(ctx.guild.channels, name="General", type=ChannelType.voice).members:
        members.append(member.name)

    print(f'members: {members}')
    # print(f'members: {discord.utils.get(ctx.guild.channels, name="General", type=ChannelType.voice).members}')
    # await ctx.send('see console')

bot.run(TOKEN)
