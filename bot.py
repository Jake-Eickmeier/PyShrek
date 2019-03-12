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
SERVER_NAME = "That next level shit"    #The name of the target server

#Adding all extensions here will prevent need to use ospath to iterate
#TODO: IMPLEMENT ospath SO THAT I DONT NEED TO MANUALLY KEEP TRACK OF THESE
extensions = ['audioManager']

#This will grab the directory that this script resides in and append the supposed
#csv file location
CSV_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "\\members_data.csv"
SERVER_REFERENCE = None     #Will be used to grab a reference to the target server
members_data = None     #We want the scope of this DataFrame to be at this level
                        #because we use it in several different places

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

    #Grab reference to target server for later applications
    for server in client.servers:
        if SERVER_NAME in str(server):
            SERVER_REFERENCE = server

    await client.change_presence(game=discord.Game(name='with data!'))  #Simple game status change

    try:    #Try reading a csv
        members_data = pd.read_csv(CSV_DIRECTORY, index_col=0)
        print("Successfully read csv")
    except:     #TODO: *SHOULD CHANGE THIS TO PARTICULAR 'NOT FOUND' EXCEPTION* If no csv is found, we will start making one
        print("Couldn't read csv")

        names = []
        for mem in SERVER_REFERENCE.members:    #Compile a list of names to add to the DataFrame
            if (str(mem.top_role) != "@everyone"):
                names.append(str(mem.top_role))

        columns = ['date', 'name', 'offline_time', 'away_time', 'online_time']
        members_data = pd.DataFrame(columns=columns)
        todays_date = str(date.today())
        for name in names:
            members_data = members_data.append({'date' : todays_date,
                                                'name' : name}, ignore_index=True)

        members_data.to_csv(CSV_DIRECTORY)  #Finally, save the newly created DataFrame as a csv
        print(members_data)


    #Start our data mining task so that we can collect information on our members
    #(this task will repeat every n seconds, where n is the sleep time at the end
    #of the function definition)
    client.loop.create_task(mine_data(SERVER_REFERENCE, members_data))

    #Save the updated data
    members_data.to_csv(CSV_DIRECTORY)

#This will check if this is the "main" file, by ensuring that it's not being
#imported for use within another script
if __name__ == '__main__':
    for extension in extensions:
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

async def mine_data(server_reference, df):  #This method defines how we collect data
    while True:
        #print("mining")
        current_datetime = str(date.today())
        #NOTE: This block of code that mines status data is temporarily disabled while I
        #do further testing
        """
        [Redacted non-working code]
        """

        df.to_csv(CSV_DIRECTORY)
        await asyncio.sleep(30)


client.run(TOKEN)
