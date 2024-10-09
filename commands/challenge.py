import discord

from datetime import datetime
from utils.api import get_random_challenge, fetch_player_progress
from database.db import add_challenge, get_current_challenge, check_challenge_status, get_all_users, finish_challenge

async def send_random_challenge(message):
    challenge = get_random_challenge()

    if challenge:

        add_challenge(
            challenge['console'], 
            challenge['game'], 
            challenge['game_id'], 
            challenge['console_image_url'], 
            challenge['game_image_url']
        )

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

async def check_current_challenge(message):
    challenge = get_current_challenge()

    if challenge:
        
        start_date = datetime.strptime(challenge['start_date'], '%Y-%m-%d %H:%M:%S.%f')
        end_date = datetime.strptime(challenge['end_date'], '%Y-%m-%d %H:%M:%S.%f')

        formatted_start_date = start_date.strftime('%d/%m/%Y %H:%M')
        formatted_end_date = end_date.strftime('%d/%m/%Y %H:%M')

        embed = discord.Embed(
            title="🎮 Desafio!",
            description=f"O desafio atual é para o jogo **{challenge['game_name']}** no console **{challenge['console_name']}**!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=challenge['console_image_url'])
        embed.set_image(url=challenge['game_image_url'])

        embed.add_field(name="Data de Início", value=formatted_start_date, inline=True)
        embed.add_field(name="Data de Fim", value=formatted_end_date, inline=True)

        await message.channel.send(embed=embed)
        return True
    else:
        return False    

async def check_challenge_progress(channel):
    challenge = check_challenge_status()

    if challenge and challenge['is_open'] == 1:
        embed = discord.Embed(
            title="🏁 Desafio Encerrado!",
            description=f"O desafio para o jogo **{challenge['game_name']}** no console **{challenge['console_name']}** terminou!",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=challenge['console_image_url'])
        embed.set_image(url=challenge['game_image_url'])

        users = get_all_users()
        champion = None
        champion_score = 0
        progress_details = []

        for user in users:
            _, ra_username = user
            progress = fetch_player_progress(ra_username, challenge['game_id'])

            if progress:
                num_achieved = progress['NumAchievedHardcore']
                total_achievements = progress['NumPossibleAchievements']
                score_achieved = progress['ScoreAchievedHardcore']
                possible_score = progress['PossibleScore']
                progress_percentage = (num_achieved / total_achievements) * 100 if total_achievements > 0 else 0

                if score_achieved > champion_score:
                    champion = ra_username
                    champion_score = score_achieved

                if progress_percentage > 0:
                    progress_details.append(
                        f"**{ra_username}**: {num_achieved}/{total_achievements} conquistas ({score_achieved}/{possible_score} pontos) - Progresso: {progress_percentage:.2f}%"
                    )

        if progress_details:
            embed.add_field(name="Progresso dos Jogadores", value="\n".join(progress_details), inline=False)
        else:
            embed.add_field(name="Progresso dos Jogadores", value="Nenhum progresso registrado.", inline=False)

        if champion:
            embed.add_field(name="🏆 Campeão", value=f"Parabéns, **{champion}**! Você foi o campeão deste desafio!", inline=False)

        await channel.send(embed=embed)

        await finish_challenge(challenge['id'])
