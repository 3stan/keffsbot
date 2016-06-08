import asyncio
import random

from HandlerBase import HandlerBase
import util

class RollHandler(HandlerBase):
    @asyncio.coroutine
    def handle(self, message):
        message_content = message.content
        tokenized_content = message_content.split()
        if len(tokenized_content) > 1:
            if util.RepresentsInt(tokenized_content[1]):
                if int(tokenized_content[1]) > 0:
                    yield from self.client.send_message(message.channel, '{} rolled {}'.format(message.author.name, random.randint(0, int(tokenized_content[1]))))
                else:
                    yield from self.client.send_message(message.channel, '{} tried to fuck up the bot. Nice try.'.format(message.author.name))
            elif util.RepresentsFloat(tokenized_content[1]):
                if float(tokenized_content[1]) > 0:
                    yield from self.client.send_message(message.channel, '{} rolled {}'.format(message.author.name, random.uniform(0, float(tokenized_content[1]))))
                else:
                    yield from self.client.send_message(message.channel, '{} tried to fuck up the bot. Nice try.'.format(message.author.name))
        else:
            yield from self.client.send_message(message.channel, '{} rolled {}'.format(message.author.name, random.randint(0, 100)))