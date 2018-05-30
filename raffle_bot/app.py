import asyncio, discord, random, os, utils
from discord.ext.commands import Bot

client = Bot(description="Raffle-Bot", command_prefix='!', pm_help = False)

# List of ready messages for the bot to utilize in the code.
r_messages = {
	"raffle_start" : "<@{}> has initiated a raffle! Write something in the chat in the next {} minutes to participate! The prize set for this raffle is '{}'!",
	"raffle_ending" : "There are only {} minute(s) remaining for <@{}>'s raffle! Write something in the chat if you wish to participate!",
	"raffle_end" : "The raffle has ended! The winner will be announced after I'm done counting!",
	"raffle_winner" : "<@{}> is the winner of the raffle initiated by <@{}>! Congratulations! The prize set for this raffle was '{}'!",
	"raffle_error_arguments" : "Sorry <@{}>, seems like you haven't passed enough arguments in! Type in '!raffle *time_in_minutes* *the_prize*!'",
	"raffle_error_time" : "Sorry <@{}>, I can only hold raffles between 10 and 30 minutes long!",
	"raffle_result_dm" : "List of the IDs of the participants: {}. Type in '<@id>' to tag the user if needed."
}

# List of roles that will be able to initialize raffles and will not be considered for winning one. 
permitted_roles = [
	'broadcaster'
]

# Function that allows for creating custom commands.
async def command(message,text):
	text = str(text)[1:]

	if utils.permission_check(message.author, permitted_roles): # Checking if the user has one of the roles in permitted_roles.
		
		try:
			if text.lower().startswith('raffle'): # Running the code associated with the !raffle command.
				time_limit = int(text.split(' ')[1])
				prize = text.split(' ')[2]

			await run_raffle(message, time_limit, prize)

		except IndexError:
			error_msg = await client.send_message(message.channel, r_messages['raffle_error_arguments'].format(message.author.id))
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
	if time_limit >= 10 and time_limit <= 30: # Default min and max time for a raffle. Replace if necessary. 
		time_limit *= 60 # Converting from seconds to minutes.
		time_remaining = int(time_limit/10)

		initial_message = await client.send_message(message.channel, r_messages['raffle_start'].format(message.author.id, time_limit, prize))
		await asyncio.sleep(time_limit - time_remaining)
		
		await client.send_message(message.channel, r_messages['raffle_ending'].format(time_remaining, message.author.id))
		await asyncio.sleep(time_remaining)

		last_message = await client.send_message(message.channel, r_messages['raffle_end'])
		winner, participants = await choose_winner(message.channel, initial_message, last_message)
		await asyncio.sleep(5)
		await client.send_message(message.channel, r_messages['raffle_winner'].format(winner, message.author.id, prize))
		await client.send_message(message.author, r_messages['raffle_result_dm'].format(participants_number))

	else:
		error_msg = await client.send_message(message.channel, r_messages['raffle_error_time'].format(message.author.id, time_limit, prize))
		await asyncio.sleep(10)
		await client.delete_message(error_msg)
		await client.delete_message(message)

# The function for finding participants and choosing the winner.
async def choose_winner(channel, initial_message, last_message):
	participants = []
	async for message in client.logs_from(channel, after=initial_message, before=last_message): # Going through every message after the raffle started and before it ended.
		if message.author.id not in participants and not utils.permission_check(message.author, permitted_roles): 
			participants.append(message.author.id) # Logging every user that sent a message during that time into a list.

	participants_number = len(participants)
	ticket = random.randint(0,participants_number)
	winner = participants[ticket]

	return winner, participants

# Triggers on every event.
@client.event
async def on_message(message):
	if message.content.startswith(client.command_prefix): # Setting up commands. You can add new commands in the commands() function at the top of the code.
		await command(message, message.content)

#client.run(os.getenv('RAFFLE_TOKEN')) # set an ENV variable RAFFLE_TOKEN to the discord token of the bot.
