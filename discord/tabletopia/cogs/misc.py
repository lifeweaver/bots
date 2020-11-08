import random
import discord
from discord import ChannelType
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Misc is online')

    @commands.command(name='quote', help='Responds with a random board game quote', brief='Board game quote')
    async def random_quote(self, ctx):
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
    async def random_number(self, ctx):
        response = random.randrange(0, 100)
        await ctx.send(response)

    @commands.command(
        name='random_player', help='Responds with a random player in the general text chat', brief='Random player',
        aliases=['rp', 'fp', 'pick', 'first_player', 'firstplayer', 'randomplayer']
    )
    async def random_player(self, ctx):
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
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')


def setup(bot):
    bot.add_cog(Misc(bot))
