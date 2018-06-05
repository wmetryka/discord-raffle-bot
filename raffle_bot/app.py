import asyncio, discord, random, os
import utils, config
from discord.ext.commands import Bot

client = Bot(description="Raffle-Bot", command_prefix='!', pm_help = False)

# Function that allows for creating custom commands.
async def command(message,text):
	text = str(text)[1:]

	if utils.permission_check(message.author, config.permitted_roles): # Checking if the user has one of the roles in permitted_roles.
		
		try:
			if text.lower().startswith('raffle'): # Running the code associated with the !raffle command.
				time_limit = int(text.split(' ')[1])
				prize = text.split(' ')[2]

			await run_raffle(message, time_limit, prize)

		except IndexError:
			error_msg = await client.send_message(message.channel, config.r_messages['raffle_error_arguments'].format(message.author.id))
			await asyncio.sleep(10)
			await client.delete_message(error_msg)
			await client.delete_message(message)	


		
	else:	# What happens if the user has no permission to use the bot.	
		error_msg = await client.send_message(message.channel, "You don't have the permission to use me!")
		await asyncio.sleep(3)
		await client.delete_message(error_msg)
		await client.delete_message(message)

# The main function for running a raffle.
async def run_raffle(message, time_limit, prize):
	if time_limit >= config.settings['min_time'] and time_limit <= config.settings['max_time']: # Default min and max time for a raffle. Replace if necessary. 
		
		if float(time_limit/10) < 1:
			time_remaining = float(time_limit/10)
		else:
			time_remaining = int(time_limit/10)

		initial_message = await client.send_message(message.channel, config.r_messages['raffle_start'].format(message.author.id, time_limit, prize))		
		time_limit *= 60 # Converting from seconds to minutes.
		await asyncio.sleep(time_limit - time_remaining)
		
		await client.send_message(message.channel, config.r_messages['raffle_ending'].format(time_remaining, message.author.id))
		await asyncio.sleep(time_remaining)

		winner, participants = await choose_winner(message.channel, initial_message, last_message)		
		
		if winner == 0: # Check if any users partook in the raffle.
			last_message = await client.send_message(message.channel, config.r_messages['raffle_end'])
			await asyncio.sleep(5)
			await client.send_message(message.channel, config.r_messages['raffle_error_no_participants'])
			await client.send_message(message.author, config.r_messages['raffle_error_no_participants'])
		else:
			await client.send_message(message.channel, config.r_messages['raffle_winner'].format(winner, message.author.id, prize))
			await client.send_message(message.author, config.r_messages['raffle_result_dm'].format(participants))

	else:
		error_msg = await client.send_message(message.channel, config.r_messages['raffle_error_time'].format(message.author.id, config.settings['min_time'], config.setting['max_time']))
		await asyncio.sleep(10)
		await client.delete_message(error_msg)
		await client.delete_message(message)

# The function for finding participants and choosing the winner.
async def choose_winner(channel, initial_message, last_message):
	participants = []
	async for message in client.logs_from(channel, after=initial_message, before=last_message): # Going through every message after the raffle started and before it ended.
		if message.author.id not in participants and not utils.permission_check(message.author, config.permitted_roles): 
			participants.append(message.author.id) # Logging every user that sent a message during that time into a list.

	winner = utils.pick_ticket(participants)

	return winner, participants

# Used to simplify the invite process. Just click the printed link.
@client.event
async def on_ready():
	print('\nInvite link: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))

# Triggers on every event.
@client.event
async def on_message(message):
	if message.content.startswith(client.command_prefix): # Setting up commands. You can add new commands in the commands() function at the top of the code.
		await command(message, message.content)

client.run(os.getenv('RAFFLE_TOKEN')) # set an ENV variable RAFFLE_TOKEN to the discord token of the bot.
