import asyncio, discord, os, datetime, sqlite3, json
import utils, config
from discord.ext.commands import Bot

client = Bot(description="Raffle-Bot", command_prefix='!', pm_help = False)

class Raffle:
	def __init__(self, message, time_limit, reward):
		self.time_limit = int(time_limit) * 60
		self.reward = reward
		self.message = message
		self.author = message.author
		self.participants = []
		self.raffle_id = 0

	# Main function where the entire raffle takes place.
	async def run_raffle(self):
		# Check if the user has permission to use the bot.
		if utils.permission_check(self.author, config.permitted_roles):
			# Check if time is within the limits.
			if self.time_limit/60 >= config.settings['min_time']\
			and self.time_limit/60 <= config.settings['max_time']: 
				
				initial_message = await client.send_message(self.message.channel,\
			 	config.r_messages['raffle_start']\
				.format(self.author.id, int(self.time_limit/60), self.reward))
				
				await asyncio.sleep(self.time_limit) # Sleep for the duration of the raffle.
				self.participants = await self.collect_participants(initial_message) 
				self.winner = utils.pick_ticket(self.participants)

				if self.winner == 0: # Check if anyone took part in the raffle.
					await client.send_message(self.message.channel,\
					 config.r_messages['raffle_error_no_participants'])
				else: # Announce the winner.
					self.use_db() # Save the raffle into the DB.
					await client.send_message(self.message.channel,\
					config.r_messages['raffle_winner'].format(self.winner, self.author.id, self.reward))
					await client.send_message(self.author,\
					config.r_messages['raffle_result_dm'].format(self.raffle_id))

			else:
				await client.send_message(self.message.channel,\
				config.r_messages['raffle_error_time']\
				.format(self.author.id, config.settings['min_time'], config.settings['max_time']))

		else:
			await client.send_message(self.message.channel,\
			config.r_messages['raffle_error_permissions'].format(self.author.id))

	# Used to gather all the participants after the raffle was started.
	async def collect_participants(self, initial_message):
		participants = []
		# Going through every message after the raffle started and before it ended.
		async for message in client.logs_from(self.message.channel, after=initial_message):
			if message.author.id not in participants\
			and not utils.permission_check(message.author, config.permitted_roles)\
			and not utils.permission_check(message.author, config.excluded_roles)\
			and message.author.id != client.user.id: 
				participants.append(message.author.id)

		return participants

	# Basic DB utilities to allow for raffle rerolls.
	def use_db(self):
		conn = sqlite3.connect('raffles.db')
		c = conn.cursor()
		self.raffle_id = utils.check_last_id()
		# Creates a table if not already present.
		c.execute('''CREATE TABLE if not exists raffles (id INTEGER PRIMARY KEY, 
		date text, participants text, winner text, reward text)''')
		# The querry values to insert data into the db.
		values = [str(datetime.datetime.today()), json.dumps(self.participants), self.winner, self.reward]
		c.execute("INSERT INTO raffles(date, participants, winner, reward) VALUES (?, ?, ?, ?)", values) 
		conn.commit()
		conn.close()

# Used to simplify the invite process. Just click the printed link.
@client.event
async def on_ready():
	print(\
	'\nInvite link: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'\
	.format(client.user.id))

# Triggers on every event.
@client.event
async def on_message(message):
	args = utils.command_strip(message)
	if message.content.startswith(client.command_prefix + 'raffle') \
	or message.content.startswith(client.command_prefix + 'reroll'):
		
		if utils.permission_check(message.author, config.permitted_roles):
			if message.content.startswith(client.command_prefix + 'raffle'):
				try:
					current_raffle = Raffle(message, args[0], args[1]) # Initiate the raffle.
					# Start up the main function, outside of the class due to asyncio limitations.
					await current_raffle.run_raffle() 
				except (IndexError, ValueError) as e:
					await client.send_message(message.channel,\
					config.r_messages['raffle_error_arguments'].format(message.author.id))

			elif message.content.startswith(client.command_prefix + 'reroll'):
				winner, reward = utils.reroll(args[0])

				await client.send_message(message.channel,\
				config.r_messages['raffle_reroll_winner'].format(args[0], winner, reward))

		else:
			await client.send_message(message.channel,\
			config.r_messages['raffle_error_permissions'].format(message.author.id))
	

client.run(os.getenv('RAFFLE_TOKEN')) # set an ENV variable RAFFLE_TOKEN to the discord token of the bot.
