# This Python file uses the following encoding: utf-8
import asyncio
import codecs
import datetime
import discord
import os
import pafy
import random
import re
import sys

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except:
        return False

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

class ChatBot(object):
    client = discord.Client()
    user_map = {}
    last_user_id_refresh = -1
    refresh_interval = 10 #seconds

    bot_deleted_messages = []

    unbannable_ids = [
        "77562181532524544",
        "88098068448157696"
    ]
    
    replacement_dict = {
        #"white": "**WHITE**",
        #"black": "*black*",
        #"^": "/\\\\" #u"\xe2\x87\xaa"
    }

    blacklisted_text = [
        "|)",
        "-)"
    ]

    user_last_msg_dict = {}

    spam_duration = 5 #seconds 

    kick_in_progress = False
    votes_left = -1
    already_voted = []
    to_kick = None
    voice_channel = None
    voice_client = None
    player = None

    music_queue = []
    current_file = ""

    def cmd_ignore(self, message):
        pass

    @asyncio.coroutine
    def cmd_roll(self, message):
        message_content = message.content
        tokenized_content = message_content.split()
        if len(tokenized_content) > 1 and RepresentsInt(tokenized_content[1]):
            if int(tokenized_content[1]) > 0:
                yield from self.client.send_message(message.channel, '{} rolled {}'.format(message.author.name, random.randint(0, int(tokenized_content[1]))))
            else:
                yield from self.client.send_message(message.channel, '{} tried to fuck up the bot. Nice try.'.format(message.author.name))
        else:
            yield from self.client.send_message(message.channel, '{} rolled {}'.format(message.author.name, random.randint(0, 100)))

    @asyncio.coroutine
    def cmd_votekick(self, message):
        if self.kick_in_progress:
            if len(message.content.split()) > 1:
                self.client.send_message(message.channel, '!votekick: Please do not try to start another votekick while one is in progress.')
            elif message.author.id in self.already_voted:
                self.client.send_message(message.channel, '!votekick: @{}: You cannot vote more than once.'.format(message.author.name))
            else:
                self.votes_left -= 1
                if self.votes_left == 0:
                    self.client.send_message(message.channel, '!votekick: Enough votes against {} has been reached. Kicking the user off the server.'.format(self.to_kick.name))
                    self.client.kick(message.channel.server, self.to_kick)
                    self.kick_in_progress = False
                    self.votes_left = -1
                    self.already_voted = []
                    self.to_kick = None
                else:
                    self.already_voted.append(message.author.id)
                    self.client.send_message(message.channel, '!votekick: {} more votes left until {} is kicked'.format(self.votes_left, self.to_kick.name))
        else:
            if not len(message.content.split()) > 1:
                self.client.send_message(message.channel, '!votekick: Please specify a user to kick')
            else:
                user = " ".join(message.content.split()[1:])
                if user[0] == '<' and user[1] == "@" and user[-1] == ">":
                    user_id = user[2:-1]
                    for key in self.user_map.keys():
                        if self.user_map[key].id == user_id:
                            user = self.user_map[key].name

                if not user in self.user_map.keys():
                    self.client.send_message(message.channel, '!votekick: User named {} does not exist.'.format(user))
                elif self.user_map[user].id in self.unbannable_ids:
                    self.client.send_message(message.channel, '!votekick: {} is an admin and cannot be kicked.'.format(user))
                else:
                    self.to_kick = self.user_map[user]
                    self.kick_in_progress = True
                    self.votes_left = 10
                    self.already_voted.append(message.author.id)
                    self.client.send_message(message.channel, '!votekick: Votekick against {} has started. {} more votes left until they are kicked.'.format(user, self.votes_left))

    @asyncio.coroutine
    def cmd_respond(self, message):
        self.client.send_message(message.channel, "SUP NIGGA")

    @asyncio.coroutine
    def cmd_emphasis(self, message):
        to_print = message.content.split()[1:]
        self.client.delete_message(message)
        self.bot_deleted_messages.append(message.id)
        self.client.send_message(message.channel, "On behalf of {}: ".format(message.author.name) + "***`" + " ".join(to_print) + "`***")

    @asyncio.coroutine
    def cmd_topic(self, message):
        topic = message.content.split()[1:]
        self.client.send_message(message.channel, "{} is updating the channel topic.".format(message.author.name))
        self.client.edit_channel(message.channel, topic = " ".join(topic))

    @asyncio.coroutine
    def cmd_commands(self, message):
        yield from self.client.send_message(message.channel, "Available commands are: {}".format(self.available_commands_dict.keys()))

    @asyncio.coroutine
    def cmd_music(self, message):
        if not(self.client.is_voice_connected()):
            self.voice_client = yield from self.client.join_voice_channel(self.voice_channel)
        youtubeURL = message.content.split()[1]
        if self.player is not None and self.player.is_playing():
            self.music_queue.append(youtubeURL)
            yield from self.client.send_message(message.channel, "Added your request to the queue".format(youtubeURL))
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
        yield from self.client.send_message(message.channel, "Current queue: {}".format(self.music_queue))

    available_commands_dict = {
        '!roll': cmd_roll,
        '!ignore': cmd_ignore,
        '!votekick': cmd_votekick,
        '!vote': cmd_votekick,
        '!sup bot': cmd_respond,
        '!emphasis': cmd_emphasis,
        '!topic': cmd_topic,
        '!commands': cmd_commands,
        "!music": cmd_music,
        "!stop": cmd_stop,
        "!queue": cmd_queue
    }

    def check_blacklist_text(self, message):
        message_content = message.content
        for text in self.blacklisted_text:
            if text in message_content:
                self.client.delete_message(message)
                self.bot_deleted_messages.append(message.id)
                self.client.send_message(message.author, "Please do not use \"{}\" in your messages.".format(text))
                return

    def check_rules(self, message):
        self.check_blacklist_text(message)

    def warn_spam(self, message):
        self.client.send_message(message.author, "Please do not spam bot commands.")

    def check_spam(self, message):
        if not message.author.id in self.user_last_msg_dict.keys():
            return True 
        else:
            return self.user_last_msg_dict[message.author.id] + self.spam_duration < unix_time(message.timestamp)

    def update_last_timestamp(self, message):
        self.user_last_msg_dict[message.author.id] = unix_time(message.timestamp)

    def process_text(self, text, original, new):
        regex = re.compile(re.escape(original), re.IGNORECASE)
        return regex.sub(new.encode('utf-8'), text)

    @asyncio.coroutine
    def execute_command(self, message):
        message_content = message.content

        for key in self.available_commands_dict:
            if message.content.startswith(key):
                yield from self.available_commands_dict[key](self, message)
                self.update_last_timestamp(message)
                return

    def sed_message(self, message):
        to_return = message.content
        for key in self.replacement_dict:
            to_return = self.process_text(to_return, key, self.replacement_dict[key])
        return to_return

    def __init__(self):
        @self.client.event
        @asyncio.coroutine
        def on_ready():
            print('Connected!')
            print('Username: ' + self.client.user.name)
            print('ID: ' + self.client.user.id)
            for server in self.client.servers:
                for member in server.members:
                    self.user_map[member.name] = member
            self.last_user_id_refresh = unix_time(datetime.datetime.utcnow().replace(microsecond=0))
            channels = self.client.get_all_channels()
            for channel in channels:
                if(channel.name == "wut"):
                    self.voice_channel = channel

        @self.client.event
        @asyncio.coroutine
        def on_message(message):
            if unix_time(message.timestamp) - self.last_user_id_refresh > self.refresh_interval:
                for server in self.client.servers:
                    for member in server.members:
                        self.user_map[member.name] = member
                self.last_user_id_refresh = unix_time(datetime.datetime.utcnow().replace(microsecond=0))

            if message.author.id != self.client.user.id:
                if (not message.channel.is_private) and (message.channel.name.startswith('triggertriggertriggertrigger') or message.channel.name.startswith('bottesting')):
                    self.check_rules(message)

                    if message.content.startswith("!"):
                        if self.check_spam(message):
                            yield from self.execute_command(message)
                            return
                        else:
                            self.warn_spam(message)
                            return

                    processed_message = self.sed_message(message)
                    if message.content != processed_message:
                        yield from self.client.delete_message(message)
                        yield from self.client.send_message(message.channel, "On behalf of {}: ".format(message.author.name) + processed_message)
                        self.bot_deleted_messages.append(message.id)

        @self.client.event
        @asyncio.coroutine
        def on_message_delete(message):
            if message.id not in self.bot_deleted_messages:
                yield from self.client.send_message(message.channel, '{}\'s message has been deleted:\n{}'.format(message.author.name, message.content))
            else:
                self.bot_deleted_messages.remove(message.id)

        discord.opus.load_opus("libopus.0.dylib")
        self.client.run(os.environ['DISCORD_SECRET'])
