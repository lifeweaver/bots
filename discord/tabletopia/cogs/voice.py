import os
import discord
from discord.ext import commands
from discord import VoiceChannel, VoiceClient
from discord import ChannelType


class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Voice is online')

    @commands.command()
    async def join(self, ctx: commands.Context):
        voice = ctx.author.voice
        if voice:
            channel = voice.channel
        else:  # Sometimes it says the message author isn't in a voice channel when they are, this is the backup
            channel = discord.utils.get(ctx.guild.channels, name="General", type=ChannelType.voice)

        if channel:
            self.voice_channel = await channel.connect()
            print(f'Connected to channel: {channel.name}')
        else:
            print(f'Author not in a voice channel')

    @commands.command()
    async def leave(self, ctx: commands.Context):
        if self.voice_channel:
            await self.voice_channel.disconnect()
        else:
            voice_client: VoiceClient
            voice_client = ctx.author.voice
            if voice_client:
                print('found voice')
                channel = voice_client.channel
                if channel:
                    print('found channel')
                    await channel.disconnect()

    @commands.command()
    async def play(self, ctx: commands.Context, url: str):
        voice_client: VoiceClient
        voice_client = ctx.author.voice
        # discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        # discord.FFmpegPCMAudio
        # voice_client.send_audio_packet()
        # voice_client.play()


def setup(bot):
    bot.add_cog(Voice(bot))

