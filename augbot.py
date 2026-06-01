import os

import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
WATCHED_USER_ID = int(os.environ['WATCHED_USER_ID'])

DEUS_EX_KEYWORDS = [
    'deus ex', 'jensen', 'augmented', 'sarif', 'illuminati',
    'mankind divided', 'human revolution', 'eidos', 'aug'
]

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
    if any(kw in content for kw in DEUS_EX_KEYWORDS):
        await message.channel.send("I never asked for this.")

client.run(TOKEN)