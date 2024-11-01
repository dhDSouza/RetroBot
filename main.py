import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
from commands.achievements import fetch_user_achievements, get_new_achievements
from commands.challenge import send_random_challenge, check_challenge_progress, check_current_challenge, updated_challenge, participate_challenge
from commands.register import registrar
from commands.profile import show_user_profile
from commands.activity import user_activity
from commands.awards import fetch_user_awards
from database.db import create_tables

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL')

intents = discord.Intents.default()
intents.message_content = True

# Usando o commands.Bot com o prefixo "!"
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'{bot.user} está pronto!')
    create_tables()

    # Iniciar as tarefas recorrentes
    check_challenge.start()
    check_for_new_achievements.start()


def get_channel():
    """Função utilitária para obter o canal configurado."""
    channel = discord.utils.get(bot.get_all_channels(), name=CHANNEL)
    if channel:
        return channel
    else:
        print("Canal não encontrado. Verifique o nome do canal.")
        return None
    
def is_in_configured_channel():
    async def predicate(ctx):
        try:
            channel = get_channel()
            if not channel:
                print("Canal configurado não encontrado.")
                return False
            return ctx.channel == channel
        except Exception as e:
            print(f"Erro ao verificar o canal configurado: {e}")
            return False
    return commands.check(predicate)

@tasks.loop(minutes=15)
async def check_challenge():
    channel = get_channel()
    if channel:
        await check_challenge_progress(channel)


@tasks.loop(hours=1)
async def check_for_new_achievements():
    channel = get_channel()
    if channel:
        await get_new_achievements(channel) 

@bot.command(name="registrar")
@is_in_configured_channel()
async def registrar_comando(ctx, *, user_message: str):
    try:
        await registrar(ctx.message, user_message)
    except Exception as e:
        print(f"Erro ao registrar: {e}")
        await ctx.send("Erro ao processar o comando de registro. Tente novamente.")


@bot.command(name="conquistas")
@is_in_configured_channel()
async def conquistas_comando(ctx):
    try:
        await fetch_user_achievements(ctx.message)
    except Exception as e:
        print(f"Erro ao buscar conquistas: {e}")
        await ctx.send("Erro ao buscar suas conquistas.")


@bot.command(name="desafio")
@is_in_configured_channel()
async def desafio_comando(ctx):
    try:
        current_challenge_exists = await check_current_challenge(ctx.message)
        if not current_challenge_exists:
            await send_random_challenge(ctx.message)
    except Exception as e:
        print(f"Erro ao iniciar desafio: {e}")
        await ctx.send("Erro ao iniciar um desafio.")


@bot.command(name="atualizar_desafio")
@is_in_configured_channel()
async def atualizar_desafio_comando(ctx):
    try:
        await updated_challenge(ctx.message)
    except Exception as e:
        print(f"Erro ao atualizar desafio: {e}")
        await ctx.send("Erro ao atualizar o desafio.")


@bot.command(name="perfil")
@is_in_configured_channel()
async def perfil_comando(ctx):
    try:
        await show_user_profile(ctx.message, ctx.author)
    except Exception as e:
        print(f"Erro ao exibir perfil: {e}")
        await ctx.send("Erro ao exibir seu perfil.")


@bot.command(name="atividade")
@is_in_configured_channel()
async def atividade_comando(ctx):
    try:
        await user_activity(ctx.message, ctx.author)
    except Exception as e:
        print(f"Erro ao buscar atividade: {e}")
        await ctx.send("Erro ao buscar sua atividade.")


@bot.command(name="ajuda")
@is_in_configured_channel()
async def ajuda(ctx):
    embed = discord.Embed(
        title="**Comandos disponíveis**",
        description="Aqui estão os comandos que você pode utilizar:",
        color=discord.Color.blue()
    )

    embed.add_field(name="**!registrar** *ra_username*", value="Registra o seu usário do RA, conforme o fornecido.", inline=False)
    embed.add_field(name="**!conquistas**", value="Exibe as conquistas do usuário nas últimas 24 horas.", inline=False)
    embed.add_field(name="**!desafio**", value="Sorteia um desafio para os usuário, caso não houver um desafio ativo.", inline=False)
    embed.add_field(name="**!atualizar_desafio**", value="Altera o desafio atual", inline=False)
    embed.add_field(name="**!participar**", value="Registra a participação no desafio atual", inline=False)
    embed.add_field(name="**!perfil**", value="Exibe o perfil do usuário no RA.", inline=False)
    embed.add_field(name="**!atividade**", value="Exibe a última atividade do usuário", inline=False)
    embed.add_field(name="**!trofeus**", value="Exibe um mosaíco com os troféus do usuário", inline=False)

    await ctx.send(embed=embed)


@bot.command(name="participar")
@is_in_configured_channel()
async def participar_desafio(ctx):
    discord_id = str(ctx.author.id)
    try:
        await participate_challenge(ctx.message, discord_id)
    except Exception as e:
        print(f"Erro ao participar do desafio: {e}")
        await ctx.send("Erro ao participar do desafio.")
        
@bot.command(name="trofeus")
@is_in_configured_channel()
async def trofeus(ctx):
    discord_id = str(ctx.author.id)
    try:
        await fetch_user_awards(ctx.message, discord_id)
    except Exception as e:
        print(f"Erro ao buscar troféus: {e}")
        await ctx.send("Erro ao buscar troféus.")

# Iniciar o bot
bot.run(DISCORD_TOKEN)
