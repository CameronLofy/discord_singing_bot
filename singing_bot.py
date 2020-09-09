#! /usr/bin/python3

import time
import discord
from config import *
from discord.ext import commands    
from discord.voice_client import VoiceClient
import asyncio
import ffmpeg

token = discord_token

song_keys = ['growup', 'carolebaskin']
growup_text = {
    "Hold on hold on hold on.": "3",
    "HOLD ON!": "1",
    "Her sister was a witch": "2", 
    "right?": "0.8", 
    "And what was HER sister?": "1.6", 
    "A PRINCESS": "1.5", 
    "THE WICKED WITCH OF THE EAST BRO": "3.2", 
    "I'm going to stab him-": "0.7",
    "You're gonna look at me":"0.6",
    "and you're gonna tell me": "0.6",
    "that I'm WRONG???": "1.2", 
    "Am I WRONG?": "1", 
    "SHE WORE A CROWN AND SHE CAME DOWN IN A BUBBLE": "2.7",
    "DOUG": "1.2",
    "Grow up bro": "1.5",
    "grow up.": "0.5",
    "Get educated bud!": "1"
}

tigerking_text = {
    "~~~~~~~~~~~~~": "2",
    "CAROLE BASKIN": "1.4",
    "Killed her": "0.6",
    "Husband": "0.4",
    "WHACKED HIM": "0.8",
    "Can't convince me": "0.6",
    "That it didn't": "0.6",
    "HAPPEN": "1.1",
    "Fed him": "0.6",
    "To tigers": "0.6",
    "THEY SNACKIN'": "1.3",
    "What's happening": "1.0",
    "C A R O L E   B A S K I N    !!!": "2"
}


ffmpeg_options = {
    'options': '-vn'
}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sing(self, ctx, arg: str):
        switcher_sound = {
            "growup"    :   'songs/wicked_witch_of_the_east.mp3',
            "carolebaskin" :   'songs/tiger_king.mp3'
        }
        switcher_text = {
            "growup": growup_text,
            "carolebaskin": tigerking_text
        }

        sound = switcher_sound.get(arg)
        text = switcher_text.get(arg)
        async with ctx.typing():
            ctx.voice_client.play(discord.FFmpegPCMAudio(sound), after=lambda e: print('done', e))
        for word in text:
            await ctx.send(word)
            time.sleep(float(text[word]))

        
        
        await ctx.voice_client.disconnect()

    @commands.command()
    async def ghana(self, ctx):
        picture_file_list ={
            'pics/ghana1.jpg': 1.5, 
            'pics/ghana2.jpg': 1.5, 
            'pics/ghana3.jpg': 1.5, 
            'pics/ghana4.jpeg': 0.2,
            'pics/ghana_says_goodbye.gif': 0
        }
    
        async with ctx.typing():
            
            ctx.voice_client.play(discord.FFmpegPCMAudio("songs/ghana.mp3"), after=lambda e: print('done', e))
        
        for pic in picture_file_list:
            await ctx.send(file=discord.File(pic))
            time.sleep(float(picture_file_list[pic]))
        

        time.sleep(12)
        await ctx.voice_client.disconnect()

    @commands.command()
    async def Help(self, ctx):
        keys = song_keys
        await ctx.send("Hello! I'm SingingBot! \nType '!sing' followed by what you want me to sing \nI only know a couple songs though :( \nHere's what I can do:")
     
        for cmnd in keys:
            await ctx.send(f'!sing {cmnd}')
        await ctx.send(f'!ghana')
   

    # Any new functins that require voice 
    # need to be added here as '@[function_name].before_invoke'
    @sing.before_invoke
    @ghana.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(Music(bot))

bot.run(token)
