import asyncio

from HandlerBase import HandlerBase

class TopicHandler(HandlerBase):
    @asyncio.coroutine
    def handle(self, message):
        topic = message.content.split()[1:]
        yield from self.client.send_message(message.channel, "{} is updating the channel topic.".format(message.author.name))
        yield from self.client.edit_channel(message.channel, topic = " ".join(topic))