import asyncio

class HandlerBase:
	def __init__(self, client):
		self.client = client