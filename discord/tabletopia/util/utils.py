import time
import discord
from discord.ext import commands


async def delete_message(ctx: commands.Context):
    time.sleep(0.5)
    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        print('Message was already deleted')
