# config.py

# List of roles that will be able to initialize raffles and will not be considered for winning one. 
permitted_roles = [
'broadcaster', # default value
]

# List of roles that will not be considered for the raffle.
excluded_roles = [
'friend', # default value
]

# Settings for running the raffle.
settings = {
'min_time' : 1, # [INT] Minimal time limit for the raffle (in minutes).
'max_time' : 30, # [INT] Maximal time limit for the raffle (in minutes).
'database' : "raffles.db", # Name of your raffles database (.db at the end)
'prefix' : "!", # Prefix for the commands on the discord server
}


# List of ready messages for the bot to utilize in the code.
r_messages = {
    "raffle_start" : "<@{}> has initiated a raffle! Type something in the chat in the next {} minute(s) to participate! The prize set for this raffle is '{}'!",
    "raffle_winner" : "<@{}> is the winner of the raffle initiated by <@{}>! Congratulations! The prize set for this raffle was '{}'!",
    "raffle_error_arguments" : "Sorry <@{}>, seems like the passed arguments are incorrect! Type in '!raffle *time_in_minutes* *the_prize*!'",
    "raffle_error_time" : "Sorry <@{}>, I can only hold raffles between {} and {} minutes long!",
    "raffle_error_no_participants" : "The raffle is now over, but no one took part in it!",
    "raffle_error_permissions" : "Sorry <@{}>, it doesn't look like you can use me...",
    "raffle_result_dm" : "You just finished raffle #{}. Type in '!reroll `ID`' if you need to choose a new winner",
    "raffle_reroll_winner" : "After rerolling the raffle #{}, the new winner is <@{}>! Congratulations on winning '{}'!",
}
