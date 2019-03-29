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
        """

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
        """

    def set_server_reference(self):
        for server in self.client.servers:
            if self.SERVER_NAME in str(server):
                #Grab reference to target server for later applications
                self.SERVER_REFERENCE = server
        print(str(self.SERVER_REFERENCE))

    def get_server_reference(self):
        return self.SERVER_REFERENCE
    def get_members_data(self):
        return self.members_data
    def get_csv_directory(self):
        return self.CSV_DIRECTORY
    """
    async def on_ready(self):
        print("onready")
        for server in self.client.servers:
            if self.SERVER_NAME in str(server):
                #Grab reference to target server for later applications
                self.SERVER_REFERENCE = server
        #print(str(self.SERVER_REFERENCE))
    """

class DataCollection:

    def __init__(self, client):
        self.client = client
        self.variables = Variables(self.client) #TODO: CHANGE THIS TO BE A LIST LATER SO THAT IT SUPPORTS MULTIPLE SERVERS SIMULTANEOUSLY

        if self.variables.get_server_reference() is not None:
            self.client.loop.create_task(self.mine_data_task(self.variables.get_server_reference(), self.variables.get_members_data()))

    async def mine_data_task(self, server_reference, df):  #This method defines how we collect data
        while True:
            print("mining")
            current_datetime = str(date.today())
            #NOTE: This block of code that mines status data is temporarily disabled while I
            #do further testing
            """
            [Redacted non-working code]
            """
            print("------------BEFORE:------------")
            print(df)
            print()
            for mem in server_reference.members:
                #print(str(mem.top_role) + "   -   @everyone")
                if (str(mem.top_role) != "@everyone"):
                    print("Triggered")
                    if ((df["name"] == str(mem.top_role)).any()):   # RESUME HERE TODO
                        #If there are more than 0 rows where the name and date of the member we're checking are present,
                        #then the row exists
                        if (len(df.loc[(df["name"] == str(mem.top_role)) & (df["date"] == current_datetime)].index) > 0):
                            print("Row exists")
                        else:       #Create a row for this member for today's date
                            df = df.append({'date' : current_datetime,
                                            'name' : mem.top_role}, ignore_index=True)
                    else:       #Create a row for this member for today's date
                        df = df.append({'date' : current_datetime,
                                        'name' : mem.top_role}, ignore_index=True)
                    df.fillna(0, inplace = True)    #I'd rather leave as NaN because I'm not sure of the performance implications,
                    #but I'm doing this as a temporary workaround to 'index out of bounds' issues with iloc due to floats, which
                    #are required to keep the NaN values in there.
                    if (str(mem.status) == "online"):
                        #print("1")
                        #print((df.loc[(df['date'] == current_datetime) & (df['name'] == mem.top_role), 'online_time']))
                        #if ((df.loc[(df['date'] == current_datetime) & (df['name'] == mem.top_role), 'online_time']).isnull()):
                        #if (pd.isnull(df.loc[(df['date'] == current_datetime) & (df['name'] == mem.top_role), 'online_time']).iloc[0]):
                        #print(pd.isnull(df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'online_time']))
                        #print("length...: " + str(len(pd.isnull(df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'online_time']))))
                        """
                        if (len(pd.isnull(df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'online_time'])) <= 0):
                            df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'online_time'] = 1
                            print("~~~is null~~~")
                            print(df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'online_time'])
                        else:
                        """
                        df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'online_time'] += 1
                        """
                            print("@@@is NOT null@@@")
                            print(df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'online_time'])
                        """
                    elif (str(mem.status) == "offline"):
                        #print("2")
                        """
                        if (len(pd.isnull(df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'offline_time'])) <= 0):
                            df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'offline_time'] = 1
                        else:
                        """
                        df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'offline_time'] += 1

                    elif (str(mem.status) == "idle"):
                        #print("3")
                        """
                        if (len(pd.isnull(df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'away_time'])) <= 0):
                            df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'away_time'] = 1
                        else:
                        """
                        df.loc[(df['date'] == current_datetime) & (df['name'] == str(mem.top_role)), 'away_time'] += 1


            df.to_csv(self.variables.get_csv_directory())
            await asyncio.sleep(5)

    async def on_ready(self):
        print(' R E A D Y ')    #Just for my own reference when this starts excecuting

        data_miner = DataCollection(self.client)    #TODO: MOVE CLIENT LOOP TASK TO A FUNCTION THAT CAN BE CALLED AFTER
        data_miner.variables.set_server_reference() #      SERVE REFERENCE IS SET INSTEAD OF IN __INIT__


def setup(client):
    client.add_cog(DataCollection(client))
