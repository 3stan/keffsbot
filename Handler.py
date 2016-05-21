import asyncio

from handlers import *

class Handler(object):
    client = None

    available_commands = []
    available_commands_dict = {}

    @asyncio.coroutine
    def handle(self, message):
        message_content = message.content

        for key in self.available_commands_dict:
            if message.content.startswith(key):
                yield from self.available_commands_dict[key].handle(message)

    def __init__(self, discord_client):
        self.client = discord_client
        server = list(self.client.servers)[0]
        roll_handler = RollHandler.RollHandler(self.client)
        #ignore_handler = IgnoreHandler.IgnoreHandler(self.client)
        topic_handler = TopicHandler.TopicHandler(self.client)
        commands_handler = CommandsHandler.CommandsHandler(self.client)
        music_handler = MusicHandler.MusicHandler(self.client, server)
        self.available_commands_dict = {
            '!roll': roll_handler,
            #'!ignore': ignore_handler,
            #'!votekick': cmd_votekick,
            #'!vote': cmd_votekick,
            '!topic': topic_handler,
            '!commands': commands_handler,
            "!music": music_handler,
            "!stop": music_handler,
            "!queue": music_handler
        }

        commands_handler.update_commands(self.available_commands_dict.keys())
