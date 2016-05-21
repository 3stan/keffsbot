def VotekickHandler(object):
	# @asyncio.coroutine
 #    def cmd_votekick(self, message):
 #        if self.kick_in_progress:
 #            if len(message.content.split()) > 1:
 #                self.client.send_message(message.channel, '!votekick: Please do not try to start another votekick while one is in progress.')
 #            elif message.author.id in self.already_voted:
 #                self.client.send_message(message.channel, '!votekick: @{}: You cannot vote more than once.'.format(message.author.name))
 #            else:
 #                self.votes_left -= 1
 #                if self.votes_left == 0:
 #                    self.client.send_message(message.channel, '!votekick: Enough votes against {} has been reached. Kicking the user off the server.'.format(self.to_kick.name))
 #                    self.client.kick(message.channel.server, self.to_kick)
 #                    self.kick_in_progress = False
 #                    self.votes_left = -1
 #                    self.already_voted = []
 #                    self.to_kick = None
 #                else:
 #                    self.already_voted.append(message.author.id)
 #                    self.client.send_message(message.channel, '!votekick: {} more votes left until {} is kicked'.format(self.votes_left, self.to_kick.name))
 #        else:
 #            if not len(message.content.split()) > 1:
 #                self.client.send_message(message.channel, '!votekick: Please specify a user to kick')
 #            else:
 #                user = " ".join(message.content.split()[1:])
 #                if user[0] == '<' and user[1] == "@" and user[-1] == ">":
 #                    user_id = user[2:-1]
 #                    for key in self.user_map.keys():
 #                        if self.user_map[key].id == user_id:
 #                            user = self.user_map[key].name

 #                if not user in self.user_map.keys():
 #                    self.client.send_message(message.channel, '!votekick: User named {} does not exist.'.format(user))
 #                elif self.user_map[user].id in self.unbannable_ids:
 #                    self.client.send_message(message.channel, '!votekick: {} is an admin and cannot be kicked.'.format(user))
 #                else:
 #                    self.to_kick = self.user_map[user]
 #                    self.kick_in_progress = True
 #                    self.votes_left = 10
 #                    self.already_voted.append(message.author.id)
 #                    self.client.send_message(message.channel, '!votekick: Votekick against {} has started. {} more votes left until they are kicked.'.format(user, self.votes_left))

	def __init__(self):
		pass