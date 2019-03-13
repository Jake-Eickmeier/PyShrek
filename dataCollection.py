import discord
from discord.ext import commands
import pandas as pd
import asyncio
import os.path
from datetime import date

"""
#This will grab the directory that this script resides in and append the supposed
#csv file location
CSV_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "\\members_data.csv"
SERVER_NAME = "That next level shit"    #The name of the target server
SERVER_REFERENCE = None     #Will be used to grab a reference to the target server
members_data = None     #We want the scope of this DataFrame to be at this level
                        #because we use it in several different places
"""


class Variables:    #Will hold/initialize all of the constant variables/references for DataCollection
    def __init__(self, client):
        self.client = client
        self.CSV_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "\\members_data.csv"
        self.SERVER_NAME = "That next level shit"    #The name of the target server
        self.SERVER_REFERENCE = None     #Will be used to grab a reference to the target server
        self.members_data = None     #We want the scope of this DataFrame to be at this level
                                #because we use it in several different places

        for server in self.client.servers:
            if self.SERVER_NAME in str(server):
                #Grab reference to target server for later applications
                self.SERVER_REFERENCE = server
                #self.data_collector = self.client.loop.create_task(self.mine_data_task(SERVER_REFERENCE, members_data))

        try:    #Try reading a csv
            self.members_data = pd.read_csv(self.CSV_DIRECTORY, index_col=0)
            print("Successfully read csv")
        except:     #TODO: *SHOULD CHANGE THIS TO PARTICULAR 'NOT FOUND' EXCEPTION* If no csv is found, we will start making one
            print("Couldn't read csv")

            names = []
            for mem in self.SERVER_REFERENCE.members:    #Compile a list of names to add to the DataFrame
                if (str(mem.top_role) != "@everyone"):
                    names.append(str(mem.top_role))

            columns = ['date', 'name', 'offline_time', 'away_time', 'online_time']
            self.members_data = pd.DataFrame(columns=columns)
            todays_date = str(date.today())
            for name in names:
                self.members_data = members_data.append({'date' : todays_date,
                                                    'name' : name}, ignore_index=True)

            self.members_data.to_csv(self.CSV_DIRECTORY)  #Finally, save the newly created DataFrame as a csv
            #print(members_data)

    def get_server_reference(self):
        return self.SERVER_REFERENCE
    def get_members_data(self):
        return self.members_data
    def get_csv_directory(self):
        return self.CSV_DIRECTORY

class DataCollection:

    def __init__(self, client):
        self.client = client
        self.variables = Variables(self.client) #TODO: CHANGE THIS TO BE A LIST LATER SO THAT IT SUPPORTS MULTIPLE SERVERS SIMULTANEOUSLY

        if self.variables.get_server_reference() is not None:
            self.client.loop.create_task(self.mine_data_task(self.variables.get_server_reference(), self.variables.get_members_data()))

    async def mine_data_task(self, server_reference, df):  #This method defines how we collect data
        while True:
            print("mining")
            #current_datetime = str(date.today())
            #NOTE: This block of code that mines status data is temporarily disabled while I
            #do further testing
            """
            [Redacted non-working code]
            """

            df.to_csv(self.variables.get_csv_directory())
            await asyncio.sleep(5)

    async def on_ready(self):
        print(' R E A D Y ')    #Just for my own reference when this starts excecuting
        data_miner = DataCollection(self.client)


def setup(client):
    client.add_cog(DataCollection(client))
