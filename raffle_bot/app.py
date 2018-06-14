import asyncio, discord, os
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

    # Main function where the entire raffle takes place.
    async def run_raffle(self):
        if utils.permission_check(self.author, config.permitted_roles): # Check if the user has permission to use the bot.
            if self.time_limit/60 >= config.settings['min_time']\
            and self.time_limit/60 <= config.settings['max_time']: # Check if time is within the limits.
                
                initial_message = await client.send_message(self.message.channel,\
                config.r_messages['raffle_start']\
                .format(self.author.id, int(self.time_limit/60), self.reward))
                
                await asyncio.sleep(self.time_limit) # Sleep for the duration of the raffle.
                self.participants = await self.collect_participants(initial_message) 
                winner = utils.pick_ticket(self.participants)

                if winner == 0: # Check if anyone took part in the raffle.
                    await client.send_message(self.message.channel,\
                     config.r_messages['raffle_error_no_participants'])
                else: # Announce the winner.
                    await client.send_message(self.message.channel,\
                    config.r_messages['raffle_winner'].format(winner, self.author.id, self.reward))
                    await client.send_message(self.author,\
                    config.r_messages['raffle_result_dm'].format(self.participants))
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
        async for message in client.logs_from(self.message.channel, after=initial_message): # Going through every message after the raffle started and before it ended.
            if message.author.id not in participants\
            and not utils.permission_check(message.author, config.permitted_roles)\
            and not utils.permission_check(message.author, config.excluded_roles)\
            and message.author.id != client.user.id: 
                participants.append(message.author.id) # Logging every user that sent a message during that time into a list.

        return participants


# Used to simplify the invite process. Just click the printed link.
@client.event
async def on_ready():
    print('\nInvite link: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))

# Triggers on every event.
@client.event
async def on_message(message):
    if message.content.startswith(client.command_prefix + 'raffle'): # Setting up commands. You can add new commands in the commands() function at the top of the code.
        args = utils.command_strip(message)
        try:
            current_raffle = Raffle(message, args[0], args[1]) # Initiate the raffle.
            await current_raffle.run_raffle() # Start up the main function, outside of the class due to asyncio limitations.
        except:
            await client.send_message(message.channel,\
            config.r_messages['raffle_error_arguments'].format(message.author.id))

client.run(os.getenv('RAFFLE_TOKEN')) # set an ENV variable RAFFLE_TOKEN to the discord token of the bot.