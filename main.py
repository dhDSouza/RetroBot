import discord
from discord import Message

from dotenv import load_dotenv
import os

from commands.achievements import fetch_user_achievements, send_random_challenge
from commands.register import registrar
from database.db import create_tables

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} está pronto!')

    create_tables()

@client.event
async def on_message(message: Message):
    if not message.content.startswith("!"):
        return
    if message.author == client.user:
        return
    
    arguments = message.content.split(" ")
    command = arguments[0]

    if command == "!registrar":
        try:
            user_message = arguments[1]
            await registrar(message, user_message)
        except:
            return
    elif command == "!conquistas":
        await fetch_user_achievements(message)
        return
    elif command == "!desafio":
        await send_random_challenge(message)
        return
    
    return

client.run(DISCORD_TOKEN)
