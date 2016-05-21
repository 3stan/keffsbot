# This Python file uses the following encoding: utf-8

# Common libraries
import asyncio
import codecs
import datetime
import discord
import os
import pafy
import random
import re
import sys

# Custom libraries
import Handler
import util

class ChatBot(object):
    client = discord.Client()
    handler = None

    def __init__(self):
        @self.client.event
        @asyncio.coroutine
        def on_ready():
            self.handler = Handler.Handler(self.client)
            print('Successfully connected!')
            print('Username: ' + self.client.user.name)
            print('ID: ' + self.client.user.id)

        @self.client.event
        @asyncio.coroutine
        def on_message(message):
            if message.author.id != self.client.user.id and message.content.startswith("!"):
                yield from self.handler.handle(message)


        #discord.opus.load_opus("libs/libopus.0.dylib") #MacOS
        discord.opus.load_opus("libs/libopus.so.0.5.2") #Linux
        self.client.run(os.environ['DISCORD_SECRET'])
        #self.client.run('3stan.jung+discordbot@gmail.com', '')
