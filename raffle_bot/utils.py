import random, sqlite3, json
import config

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

def check_last_id():
    conn = sqlite3.connect(config.database)
    c = conn.cursor()
    c.execute("SELECT id FROM raffles ORDER BY id DESC LIMIT 1")

    id = c.fetchall()[0][0]
    conn.close()

    return id

# Rerolls a raffle for a new winner.
def reroll(raffle_id):
    conn = sqlite3.connect(config.database)
    c = conn.cursor()

    # Fetching all the information
    c.execute("SELECT participants FROM raffles WHERE id=?", raffle_id)
    participants = json.loads(list(c.fetchone())[0])
    c.execute("SELECT winner FROM raffles WHERE id=?", raffle_id)
    winner = c.fetchone()[0]
    c.execute("SELECT reward FROM raffles WHERE id=?", raffle_id)
    reward = c.fetchone()[0]
    # Rerolling the winner
    participants.remove(winner)
    new_winner = participants[random.randint(0, len(participants)-1)]

    conn.close()

    return new_winner, reward