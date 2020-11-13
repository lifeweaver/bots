import os
from ..util import utils
import time
import youtube_dl
import discord
from discord.ext import commands
from discord import VoiceChannel, VoiceClient
from discord import ChannelType

HOME = os.getenv("DISCORD_BOT_HOME") + '/tabletopiaHelper'
MP3_LOCATION = f'{HOME}/mp3'


async def end_of_music(self, ctx: commands.Context, name: str):
    print(f'{name} has finished playing')


class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Voice is online')

    @commands.command()
    async def join(self, ctx: commands.Context):
        await utils.delete_message(ctx)
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
        await utils.delete_message(ctx)

        if self.voice_channel:
            await self.voice_channel.disconnect()
        else:
            voice_client: VoiceClient
            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice_client:
                await voice_client.disconnect()

    @commands.command()
    async def play(self, ctx: commands.Context, url: str):
        await utils.delete_message(ctx)
        voice_client: VoiceClient
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        current_file = f'{MP3_LOCATION}/song.mp3'
        song_there = os.path.isfile(current_file)

        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return

        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            voice_client = await channel.connect()

        try:
            if song_there:
                os.remove(current_file)
                print('Removed old song file')
        except PermissionError:
            print('Trying to delete song file, but it is being played')
            await ctx.send('ERROR: Music playing')
            return

        await ctx.send('Getting everything ready now')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{MP3_LOCATION}/%(title)s.%(ext)s',
            'noplaylist': True,
            'continue_dl': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],

        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print('Downloading audio now\n')
                ydl.cache.remove()
                info_dict = ydl.extract_info(url, download=False)
                ydl.prepare_filename(info_dict)
                ydl.download([url])
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError) as e:
            print(e)
            await ctx.send('Download error')
            return

        for file in os.listdir(f'{MP3_LOCATION}'):
            if file.endswith('.mp3'):
                name = file
                print(f'Renamed File: {file}\n')
                os.rename(f'{MP3_LOCATION}/{file}', current_file)

        time_to_wait = 10
        time_counter = 0
        while not os.path.isfile(current_file):
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:
                break

        voice_client.play(discord.FFmpegPCMAudio(current_file), after=await end_of_music(self, ctx, name))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source, volume=0.3)

        nname = name.rsplit('-', 2)
        await ctx.send(f'Playing {nname[0]}')

    @commands.command()
    async def stop(self, ctx: commands.Context):
        await utils.delete_message(ctx)
        voice_client: VoiceClient
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send('Playing stopped')
        else:
            await ctx.send('Not playing')

    @commands.command()
    async def pause(self, ctx: commands.Context):
        await utils.delete_message(ctx)
        voice_client: VoiceClient
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            if voice_client.is_paused():
                await ctx.send('Already paused')
            else:
                voice_client.pause()
                await ctx.send('Pausing playing')
        else:
            await ctx.send('Nothing is playing')

    @commands.command()
    async def resume(self, ctx: commands.Context):
        await utils.delete_message(ctx)
        voice_client: VoiceClient
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            await ctx.send('Already playing')
            return

        if voice_client.is_paused():
            voice_client.resume()
            await ctx.send('Playing resumed')
        else:
            await ctx.send('Nothing is paused')

    @commands.command(name='jeopardy', aliases=['j', 'waiting'])
    async def jeopardy(self, ctx: commands.Context):
        await self.play(ctx, 'https://www.youtube.com/watch?v=B3lLYOGDsts')


def setup(bot):
    bot.add_cog(Voice(bot))

