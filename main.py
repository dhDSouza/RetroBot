import discord
from discord import Message

from dotenv import load_dotenv
import os

from commands.achievements import fetch_user_achievements
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

    await create_tables()

@client.event
async def on_message(message: Message):
    if not message.content.startswith("!"):
        return
    if message.author == client.user:
        return
    
    arguments = message.content.split(" ")
    try:    
        command = arguments[0]
        user_message = arguments[1]
    except IndexError:
        await message.channel.send("Por favor, forneça o nome de usuário. Exemplo: `!registrar seu_usuario`.")
        return

    if command == "!registrar":
        await registrar(message, user_message)
        return
    elif command == "!conquistas":
        await fetch_user_achievements(message)
        return
    
    return

client.run(DISCORD_TOKEN)
