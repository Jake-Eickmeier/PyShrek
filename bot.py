# -*- coding: utf-8 -*-
"""
TO RUN THIS, need to run command: python -m pip install -U discord.py[voice]
(obtains the required library, "discord.py")
If not using Anaconda, may need to install Pandas using "pip install pandas"

FOR AUDIO PLAYER TO WORK:
- Need to install ffmpeg and set an environment variable!
- Furthermore, run "python -m pip install -U youtube_dl" to get youtube_dl

Also, this script uses a pickle file called "bot_info_dict" in the obj directory.
This file is used to fetch your TOKEN, which is confidential and should be hidden from others.
Simply create a "bot_info_dict.pkl" file with a dict containing: { "TOKEN" : <insert token here> }

@Author Jake Eickmeier
Made with python 3.6.7

IDEAS:
1. PIE GRAPH FOR GAMES PLAYED
2. GRAPH OF PEAK HOURS
"""

import discord
import asyncio
import os.path
import pandas as pd
import pickle
import youtube_dl
from discord.ext import commands
from datetime import date

client = discord.Client()
client = commands.Bot(command_prefix = '~')

#Adding all extensions here will prevent need to use ospath to iterate
#TODO: IMPLEMENT ospath SO THAT I DONT NEED TO MANUALLY KEEP TRACK OF THESE
extensions = ['audioManager', 'dataCollection']


def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

"""
#If still needing to create pickle file, here's the necessary code:
infoDict = {"TOKEN" : ""}
save_obj(infoDict, "bot_info_dict")
"""

#Using pickle for this will allow me to hide my token using .gitignore so that
#observers of my code can't ship altered code to my own servers.
TOKEN = load_obj("bot_info_dict")["TOKEN"]


@client.event
async def on_ready():
    print("Bot is ready!")
    await client.change_presence(game=discord.Game(name='with data!'))  #Simple game status change

#This will check if this is the "main" file, by ensuring that it's not being
#imported for use within another script
if __name__ == '__main__':
    for extension in extensions:
        print('Extension: {}'.format(extension))
        try:
            client.load_extension(extension)
            print('{} successfully loaded.'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

#This is the notation for the user to declare commands to the bot
#In this example, the user would type "~ping" in the chat to recieve the output
@client.command()
async def ping():
    await client.say('PONG')


client.run(TOKEN)
