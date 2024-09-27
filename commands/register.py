from discord import Message
from commands.achievements import register_ra_user

async def registrar(message: Message, usuario):
    try:
        await register_ra_user(message, usuario)
        return
    except:
        await message.channel.send("Por favor, forneça o nome de usuário. Exemplo: `!registrar seu_usuario`.")
        return