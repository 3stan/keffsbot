import asyncio

from HandlerBase import HandlerBase

class CommandsHandler(HandlerBase):
    commands = []

    @asyncio.coroutine
    def handle(self, message):
        yield from self.client.send_message(message.channel, "Available commands are: {}".format(self.commands))

    def update_commands(self, commands):
        self.commands = commands      