import random
from ..util import utils
import requests
import bs4
import discord
from discord import ChannelType
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # TODO: return title and dictionary with how to play youtube video if it exists
    # as a backup search youtube?
    def get_game_info(self, message: discord.Message):
        base_url = 'https://tabletopia.com'
        selector = "._en-flag.game-rules"
        room = f'{base_url}/playground/playgroundrooms/room?roomShortUrl={message.content[1:]}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'
        }
        res = requests.get(f'{room}', headers=headers)
        text = bs4.BeautifulSoup(res.text, 'html.parser')
        if res.status_code != requests.codes.ok or not text.select(selector):
            print(
                f'Request response code was {res.status_code} for URL: {res.request.url}, or could not find '
                'rules: ' + str(len(text.select(selector)))
            )
            return 'Failed to find game'

        return 'Rules: ' + text.select(selector)[0].attrs['href']

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Misc is online')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content[0] == '#':
            print('running on_message')
            await message.channel.send(self.get_game_info(message))

        # Uncomment if you don't have this line somewhere else on the bot
        # await self.bot.process_commands(message)

    # Commands
    @commands.command(name='quote', help='Responds with a random board game quote', brief='Board game quote')
    async def random_quote(self, ctx: commands.Context):
        await utils.delete_message(ctx)
        board_game_quotes = [
            '"Bomb it, pave it, make a parking lot out of it!" -- Anon.',
            '"The meek shall inherit the earth. The rest of us are going to the stars!" -- Anon.',
            '"Nuke em till they glow, and shoot em in the dark!" -- Anon.',
            '"Cards are war, in disguise of a sport." -- Charles Lamb',
            '"Lose your first 50 games as quickly as possible." -- Go proverb',
            '"If you\'re not prepared to lose every friend you have over a board game, you\'re not playing hard '
            'enough." -- Anon.',
            '"Never bored with a board game" -- Anon.',
        ]

        response = random.choice(board_game_quotes)
        await ctx.send(response)

    @commands.command(name='random', help='Responds with a random number between 0 and 100', brief='Random number')
    async def random_number(self, ctx: commands.Context):
        await utils.delete_message(ctx)
        response = random.randrange(0, 100)
        await ctx.send(response)

    @commands.command(
        name='random_player', help='Responds with a random player in the general text chat', brief='Random player',
        aliases=['rp', 'fp', 'pick', 'first_player', 'firstplayer', 'randomplayer']
    )
    async def random_player(self, ctx: commands.Context):
        await utils.delete_message(ctx)
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

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await utils.delete_message(ctx)
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def rules(self, ctx: commands.Context):
        await utils.delete_message(ctx)
        # look at history in the form of a list
        messages = await ctx.channel.history().flatten()
        message = next(message for message in messages if message.content[0] == '#')
        print('running rules command')
        await ctx.send(self.get_game_info(message))


def setup(bot):
    bot.add_cog(Misc(bot))
