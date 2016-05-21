import asyncio
import pafy

from HandlerBase import HandlerBase

class MusicHandler(HandlerBase):
    allowed_channel = "music"

    server = None
    voice_channel = None

    voice_client = None
    player = None

    music_queue = []
    music_dict = {}
    current_file = ""

    @asyncio.coroutine
    def cmd_music(self, message):
        if not(self.client.is_voice_connected(self.server)):
            self.voice_client = yield from self.client.join_voice_channel(self.voice_channel)
        youtubeURL = message.content.split()[1]
        if self.player is not None and self.player.is_playing():
            video = pafy.new(youtubeURL)
            self.music_queue.append(youtubeURL)
            self.music_dict[youtubeURL] = video.title
            yield from self.client.send_message(message.channel, "Added {} to the queue (Requested by {})".format(video.title, message.author.name))
        else:
            video = pafy.new(youtubeURL)
            bestaudio = video.getbestaudio()
            title = bestaudio.download()
            self.create_player_and_play(title)

    def after_routine(self):
        os.remove(self.current_file)
        if(len(self.music_queue) > 0):
            nextSong = self.music_queue[0]
            self.music_queue = self.music_queue[1:]
            video = pafy.new(nextSong)
            bestaudio = video.getbestaudio()
            title = bestaudio.download()
            self.create_player_and_play(title)

    def create_player_and_play(self, title):
        self.current_file = title
        self.player = self.voice_client.create_ffmpeg_player(title, after = self.after_routine, options = '-af "volume=0.25"')
        self.player.start()

    @asyncio.coroutine
    def cmd_stop(self, message):
        if self.player is not None:
            self.player.stop() 

    @asyncio.coroutine
    def cmd_queue(self, message):
        to_write = "\n".join([self.music_dict[url]for url in self.music_queue])
        yield from self.client.send_message(message.channel, "Current queue: \n{}".format(to_write))

    @asyncio.coroutine
    def handle(self, message):
        if(message.channel.name == self.allowed_channel):
            if(message.content.startswith("!music")):
                yield from self.cmd_music(message)
            elif(message.content.startswith("!queue")):
                yield from self.cmd_queue(message)
            elif(message.content.startswith("!stop")):
                yield from self.cmd_stop(message)

    def __init__(self, discord_client, server):
        self.client = discord_client
        self.server = server
        channels = self.client.get_all_channels()
        for channel in channels:
            if(channel.name == "wut"):
                self.voice_channel = channel