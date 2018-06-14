import random

# A function that checks if the user has permissions to utilize the bot. 
def permission_check(user, permitted_roles): 
    auth_roles = []

    for x in user.roles:
        auth_roles.append(x.name.lower())

    for x in permitted_roles:
        if x in auth_roles:
            return True
            break
        else:
            return False

# Chooses a winner from a list of participants.
def pick_ticket(participants):
    participants_number = len(participants)
    if participants_number != 0:
        ticket = random.randint(0,participants_number-1)
        winner = participants[ticket]
    else:
        winner = 0

    return winner

# Returns arguments from command calls.
def command_strip(message):
    args = []
    for x in range(message.content.count(' ')):
        args.append(message.content.split(' ')[x+1])

    return args