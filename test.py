"""
#A BASIC EXAMPLE OF HOW TO SET UP COROUTINES IN COGS

import discord
from discord.ext import commands
import asyncio

class Class:

    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self.taskName())

    async def taskName(self):
        while True:
            print("BLAH")
            await asyncio.sleep(5)

def setup(client):
    client.add_cog(Class(client))
"""
