import discord

from database.db import register_user, get_ra_username
from utils.api import get_recent_achievements, get_random_challenge

async def register_ra_user(message, ra_username):
    register_user(str(message.author.id), ra_username)
    await message.channel.send(f"{message.author.mention}, seu usuário `{ra_username}` foi registrado com sucesso!")

async def fetch_user_achievements(message):
    ra_username = get_ra_username(str(message.author.id))
    if ra_username:
        achievements = get_recent_achievements(ra_username)
        if achievements:
            for ach in achievements:
                
                hardcore_status = "Hardcore" if ach['HardcoreMode'] == 1 else "Softcore"
                game_icon_url = f"https://retroachievements.org{ach['GameIcon']}"
                achievement_icon_url = f"https://retroachievements.org{ach['BadgeURL']}"
                
                embed = discord.Embed(
                    title = f"🏆 {ach['Title']}",
                    description = f"*{ach['Description']}*",
                    color = discord.Color.gold() if hardcore_status == "Hardcore" else discord.Color.dark_gray()
                )
                
                embed.set_image(url = game_icon_url)
                embed.set_thumbnail(url = achievement_icon_url)
                embed.add_field(name = "Points", value = f"{ach['Points']} ({ach['TrueRatio']})", inline = False)
                embed.add_field(name = "Unloked in", value = ach['Date'], inline = False)
                embed.add_field(name = "Game", value = ach['GameTitle'], inline = True)
                
                await message.channel.send(embed=embed)
        else:
            await message.channel.send(f"Não consegui buscar as conquistas de `{ra_username}`.")
    else:
        await message.channel.send("Você ainda não registrou seu usuário. Use o comando `!registrar <seu_usuario>` para registrar.")

async def send_random_challenge(message):
    challenge = get_random_challenge()

    if challenge:
        embed = discord.Embed(
            title="🎮 Desafio RetroAchievements!",
            description=f"Console sorteado: **{challenge['console']}**",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=challenge['console_image_url'])
        embed.add_field(name="Jogo sorteado", value=challenge['game'], inline=False)
        embed.set_image(url=challenge['game_image_url'])
        await message.channel.send(embed=embed)
    else:
        await message.channel.send("Não consegui sortear um desafio no momento. Tente novamente mais tarde.")