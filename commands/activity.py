import discord

from database.db import get_ra_username
from utils.api import fetch_user_profile, get_last_game_played
from utils.date import convert_utc_to_brt

async def user_activity(message, username):
    ra_username = get_ra_username(username.id)

    if ra_username:
        activity = fetch_user_profile(ra_username)
        last_game_played = get_last_game_played(ra_username)

        if activity and last_game_played:
            
            if isinstance(last_game_played, list) and len(last_game_played) > 0:
                last_game_played = last_game_played[0]
                last_played = convert_utc_to_brt(last_game_played['LastPlayed'])

                embed = discord.Embed(
                    title=f"{last_game_played.get('Title', 'Jogo Desconhecido')}",
                    url=f"https://retroachievements.org/game/{activity.get('LastGameID')}",
                    color=discord.Color.gold()
                )
                embed.set_thumbnail(url=f"https://retroachievements.org{last_game_played.get('ImageIcon', '')}")
                embed.add_field(name="Console", value=f"{last_game_played.get('ConsoleName', 'Desconhecido')}", inline=False)
                embed.add_field(name="Jogado por último", value=last_played, inline=False)
                embed.add_field(name="Atividade Atual", value=activity.get('RichPresenceMsg', 'Nenhuma atividade disponível'), inline=False)

                await message.channel.send(embed = embed)
            else:
                await message.channel.send("Não foi possível obter os detalhes do último jogo jogado.")
        else:
            await message.channel.send("Não foi possível encontrar a última atividade do usuário.")
    else:
        await message.channel.send("Você ainda não registrou seu usuário. Use o comando `!registrar <seu_usuario>` para registrar.")
