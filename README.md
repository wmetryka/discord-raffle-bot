# discord-raffle-bot
A simple bot for holding real time raffles on Discord.

## Requirements
### Python 3.0 or newer.
* [discord.py](https://github.com/Rapptz/discord.py) library

## Setup and Running
### Setup
* Add roles with the permission to use the bot to `config.py`.
* Grant the role to the user permitted to run a raffle.

### Running
```
$ git clone https://github.com/Jestemkioskiem/discord-raffle-bot
$ cd discord-raffle-bot
$ virtualenv -p python3.6 discord-raffle-bot-env
$ source discord-raffle-bot-env/bin/activate
$ pip install -r requirements.txt
$ nohup python discord-raffle-bot/app.py
```

## Usage

### Starting a raffle
```!raffle <time limit in minutes> <full description of prize>```

ex.
```!raffle 10 '100$'``` will start a 10 minutes raffle for 100$.
