import discord
import os
import asyncio

from discord import Message
from dotenv import load_dotenv
from commands.achievements import fetch_user_achievements
from commands.challenge import send_random_challenge, check_challenge_progress, check_current_challenge
from commands.register import registrar
from commands.profile import show_user_profile
from database.db import create_tables

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} está pronto!')

    create_tables()

    # Função para verificar a cada 15 minutos se o desafio foi finalizado.
    async def check_challenge():
        channel = discord.utils.get(client.get_all_channels(), name=CHANNEL)
        if channel:
            while True:
                await check_challenge_progress(channel)
                await asyncio.sleep(900)
        else:
            print("Canal não encontrado. Verifique o nome do canal.")

    client.loop.create_task(check_challenge())  

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
        current_challenge_exists = await check_current_challenge(message)
        if not current_challenge_exists:
            await send_random_challenge(message)
        return
    elif command == "!perfil":
        await show_user_profile(message, message.author)
        return
    
    return

client.run(DISCORD_TOKEN)
