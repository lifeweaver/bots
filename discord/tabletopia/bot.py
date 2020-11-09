import os
import logging
import json
import discord
from dotenv import load_dotenv
from discord import ChannelType
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
load_dotenv()
HOME = os.getenv("DISCORD_BOT_HOME") + '/tabletopiaHelper'


with open(HOME + '/auth.json') as f:
    TOKEN = json.loads(f.read())['token']

with open(HOME + '/package.json') as f:
    PACKAGE = json.loads(f.read())

intents = discord.Intents(messages=True, guilds=True, members=True, presences=True, voice_states=True)
bot = commands.Bot(command_prefix='\\', intents=intents)

# TODO:
# perhaps after getting the games look up ratings for the games.
# command/loop to follow game news site? - probably not
# command ascii art?


def cog_list():
    cog_path = HOME + '/cogs'
    cog_path = cog_path if os.path.exists(cog_path) else './cogs'
    cogs = []
    for filename in os.listdir(cog_path):
        if filename.endswith('.py'):
            cogs.append(filename[:-3])

    return cogs


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')
    # TODO: pick new icon for avatar
    # https://gist.github.com/Gorialis/e89482310d74a90a946b44cf34009e88
    # https://www.youtube.com/watch?v=RK8RzuUMYt8&list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ&index=9
    # for filename in os.listdir(HOME + '/avatars'):
        # if filename.endswith('.png'):
            # do something


@bot.event
async def on_message(message: discord.Message):
    if message.content == "hello":
        await message.channel.send('Hello to you')

    await bot.process_commands(message)


@bot.command(brief='Load cog')
@commands.is_owner()
async def load(ctx: commands.Context, extension):
    bot.load_extension(f'cogs.{extension}')
    print(f'Extension {extension} loaded')


@bot.command(brief='Unload cog')
@commands.is_owner()
async def unload(ctx: commands.Context, extension):
    bot.unload_extension(f'cogs.{extension}')
    print(f'Extension {extension} unloaded')


@bot.command(brief='Reload cog')
@commands.is_owner()
async def reload(ctx: commands.Context, extension=''):
    if extension:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        print(f'Extension {extension} reloaded')
    else:
        for this_cog in cog_list():
            bot.unload_extension(f'cogs.{this_cog}')
            bot.load_extension(f'cogs.{this_cog}')
            print(f'Extension {this_cog} reloaded')


@bot.command(brief='List cogs')
@commands.is_owner()
async def list_cogs(ctx: commands.Context):
    await ctx.send('\n'.join(cog_list()))


@bot.command(name='clear', help='Clear request and response to commands', brief='Clear command messages')
@commands.is_owner()
async def clear_messages(ctx: commands.Context):
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


@bot.command(name='test', help='Used to test whatever I am currently working on', brief='test')
@commands.is_owner()
async def test_command(ctx: commands.Context):
    members = []
    for member in discord.utils.get(ctx.guild.channels, name="General", type=ChannelType.voice).members:
        members.append(member.name)

    print(f'members: {members}')
    # print(f'members: {discord.utils.get(ctx.guild.channels, name="General", type=ChannelType.voice).members}')
    # await ctx.send('see console')

# Load all cogs
for cog in cog_list():
    bot.load_extension(f'cogs.{cog}')

bot.run(TOKEN)
