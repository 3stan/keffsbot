import asyncio

from HandlerBase import HandlerBase

class IgnoreHandler(HandlerBase):
    @asyncio.coroutine
    def handle(self, message):
        pass