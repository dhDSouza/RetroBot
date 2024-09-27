import discord
from dotenv import load_dotenv
import os

from commands.achievements import register_ra_user, fetch_user_achievements
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
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!registrar'):
        try:
            ra_username = message.content.split(" ")[1]
            await register_ra_user(message, ra_username)
        except IndexError:
            await message.channel.send("Por favor, forneça o nome de usuário. Exemplo: `!registrar seu_usuario`.")

    elif message.content.startswith('!conquistas'):
        await fetch_user_achievements(message)

client.run(DISCORD_TOKEN)
