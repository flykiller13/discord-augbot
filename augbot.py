import os
import random
from datetime import date

import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
WATCHED_USER_ID = int(os.environ['WATCHED_USER_ID'])

DEUS_EX_KEYWORDS = [
    'deus ex', 'deus', 'adam', 'jensen', 'denton', 'augmented', 'sarif', 'illuminati',
    'mankind', 'divided', 'human', 'revolution', 'eidos', 'aug'
]

LAST_MENTION_FILE = 'last_mention.txt'

# 1–3 days — short streak broken
DAY_SHORT = [
    "I never asked for this.",
    "The system… it's broken. Just like your restraint.",
    "Deus Ex mentioned. Streak: dead.",
]

# 4–7 days — respectable attempt
DAY_MID = [
    "A sincere effort. Insufficient.",
    "You lasted {days} days. The illuminati are pleased.",
    "Pathetic. And yet, better than last time.",
]

# 8–13 days — impressive
DAY_HIGH = [
    "{days} days. I was beginning to have hope for you, George.",
    "The neural interface detects weakness. {days} days was a good run.",
    "Every system has a breaking point. Yours is apparently {days} days.",
]

# 14+ days — legendary
DAY_LEGENDARY = [
    "{days} days. You were supposed to be the chosen one.",
    "Helios could not have predicted this betrayal. {days} days, George.",
    "I have seen governments fall in less time than {days} days. And yet here we are.",
    "They told me augmentation would make us stronger. {days} days suggests otherwise.",
]


def get_response(days):
    if days is None:
        return "First recorded offence. It begins."
    if days <= 3:
        pool = DAY_SHORT
    elif days <= 7:
        pool = DAY_MID
    elif days <= 13:
        pool = DAY_HIGH
    else:
        pool = DAY_LEGENDARY

    return random.choice(pool).format(days=days)


def read_last_mention():
    """Return the date of the previous mention, or None if there isn't one."""
    try:
        with open(LAST_MENTION_FILE) as f:
            stamp = f.read().strip()
    except FileNotFoundError:
        return None
    if not stamp:
        return None
    try:
        return date.fromisoformat(stamp)
    except ValueError:
        return None


def write_last_mention(when):
    with open(LAST_MENTION_FILE, 'w') as f:
        f.write(when.isoformat())

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'Watching user ID: {WATCHED_USER_ID}')
    print(f'In {len(client.guilds)} server(s):')
    for g in client.guilds:
        print(f'  - {g.name} (id={g.id})')

@client.event
async def on_message(message):
    # Diagnostic: log every message the bot can see
    print(f'[msg] author={message.author} id={message.author.id} '
          f'content={message.content!r}')

    if message.author.bot:
        return
    if message.author.id != WATCHED_USER_ID:
        return

    content = message.content.lower()
    # Debug: messages starting with [kd] ("keep date") don't update last_mention.
    debug_keep_date = content.startswith('[kd]')

    if any(kw in content for kw in DEUS_EX_KEYWORDS):
        today = date.today()
        last = read_last_mention()
        if last == today:
            return
        if not debug_keep_date:
            write_last_mention(today)

        days = (today - last).days if last is not None else None
        await message.channel.send(f"{message.author.mention} {get_response(days)}")

client.run(TOKEN)