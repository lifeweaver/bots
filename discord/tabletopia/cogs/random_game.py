import time
import random
import requests
import bs4
import discord
from discord.ext import commands


class RandomGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = 'https://tabletopia.com'
        self.game_details = []

    @commands.Cog.listener()
    async def on_ready(self):
        print('Random game is online')

    @commands.command()
    async def random_game(self, ctx, max_players=5):
        res = requests.get(
            f'{self.base_url}/games?category=new-releases&minPlayersCount=1&maxPlayersCount={max_players}'
        )
        if res.status_code != requests.codes.ok:
            print(f'Initial request response code was {res.status_code} for URL: {res.request.url}')
            await ctx.send('Failed to find game')
            return

        headers = {
            'TE': 'Trailers',
            'Referer': f'{res.request.url}',
            'Cookie': res.headers['SET-COOKIE'],
            'Host': 'tabletopia.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'X-Requested-With': 'XMLHttpRequest'
        }
        current_seconds = str(time.time_ns() / 1000000)
        res = requests.get(f'{res.request.url}&_={current_seconds}', headers=headers)
        text = bs4.BeautifulSoup(res.text, 'html.parser')
        if res.status_code != requests.codes.ok or not text.select('.catalog__item'):
            print(f'Request response code was {res.status_code} for URL: {res.request.url}, or could not find games')
            await ctx.send('Failed to find game')
            return

        for catalog_item in text.select('.catalog__item'):
            self.game_details.append(
                {
                    'title': catalog_item.select('.item__title')[0].text,
                    'href': self.base_url + catalog_item.select('.item__button')[0].attrs['href']
                }
            )

        game_detail = random.choice(self.game_details)
        await ctx.send(f'{game_detail["title"]}: {game_detail["href"]}')
        return


def setup(bot):
    bot.add_cog(RandomGame(bot))



