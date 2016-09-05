import asyncio
import datetime
import os
import pafy

from HandlerBase import HandlerBase

class PaxHandler(HandlerBase):

    def days_hours_minutes(self, td):
        return td.days, td.seconds//3600, (td.seconds//60)%60

    @asyncio.coroutine
    def handle(self, message):
        delta = datetime.datetime(2016, 9, 2, hour = 17) - datetime.datetime.now()
        days, hours, minutes = self.days_hours_minutes(delta)
        seconds = delta.seconds % 60
        micro = delta.microseconds % 1000
        yield from self.client.send_message(message.channel, "PAX IS OVER.")
        #yield from self.client.send_message(message.channel, "{} days, {} hours, {} mins, {} seconds, {} MICROSECONDS left until PAX Prime!".format(days, hours, minutes, seconds, micro))