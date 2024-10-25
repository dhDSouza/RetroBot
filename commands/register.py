from discord import Message
from commands.achievements import register_ra_user

async def registrar(message: Message, usuario):
    if not usuario:
        await message.channel.send("Por favor, forneça o nome de usuário. Exemplo: `!registrar seu_usuario`.")
        return

    try:
        await register_ra_user(message, usuario)
    except Exception as e:
        await message.channel.send(f"Ocorreu um erro ao registrar: {e}")
