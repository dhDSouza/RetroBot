from database.db import register_user, get_ra_username
from utils.api import get_recent_achievements

async def register_ra_user(message, ra_username):
    register_user(str(message.author.id), ra_username)
    await message.channel.send(f"{message.author.mention}, seu usuário `{ra_username}` foi registrado com sucesso!")

async def fetch_user_achievements(message):
    ra_username = get_ra_username(str(message.author.id))
    if ra_username:
        achievements = get_recent_achievements(ra_username)
        if achievements:
            response_message = f"**Últimas conquistas de {ra_username}:**\n\n"
            for ach in achievements:
                response_message += f"🏆 **{ach['Title']}** em *{ach['GameTitle']}*\n"
            await message.channel.send(response_message)
        else:
            await message.channel.send(f"Não consegui buscar as conquistas de `{ra_username}`.")
    else:
        await message.channel.send("Você ainda não registrou seu usuário. Use o comando `!registrar <seu_usuario>` para registrar.")
