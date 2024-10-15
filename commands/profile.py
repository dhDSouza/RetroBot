import discord

from database.db import get_ra_username
from utils.api import fetch_user_profile
from utils.date import convert_utc_to_brt

async def show_user_profile(message, discord_user):
    ra_username = get_ra_username(discord_user.id)

    if not ra_username:
        await message.channel.send("Você ainda não registrou seu usuário. Use o comando `!registrar <seu_usuario>` para registrar.")
        return

    profile = fetch_user_profile(ra_username)

    if profile:
        embed = discord.Embed(
            title = f"{profile['User']}",
            url = f"https://retroachievements.org/user/{ra_username}",
            color = discord.Color.gold()
        )
        embed.set_thumbnail(url = f"https://retroachievements.org{profile['UserPic']}")
        embed.add_field(name = "Points", value = f"{profile['TotalPoints']} ({profile['TotalTruePoints']})", inline = True)
        embed.add_field(name = "Member Since", value = f"{convert_utc_to_brt(profile['MemberSince'])}", inline = True)

        if profile.get("Motto"):
            embed.add_field(name = "Motto", value = profile['Motto'], inline = False)
            
        await message.channel.send(embed=embed)
    else:
        await message.channel.send("Não foi possível busacar seu perfil no momento. Tente novamente mais tarde.")
