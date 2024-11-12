import discord
import tempfile
from PIL import Image
import requests
from io import BytesIO
from database.db import get_ra_username
from utils.api import get_awards

async def fetch_user_awards(message, discord_user):
    ra_username = get_ra_username(discord_user)
    
    if not ra_username:
        await send_registration_prompt(message)
        return
    
    awards = get_awards(ra_username)
    
    if awards:
        mastery_games = []
        beaten_games = []
        site_awards = []
        
        visible_awards = awards.get("VisibleUserAwards", [])
        
        if visible_awards:
            for award in visible_awards:
                if award['ConsoleName'] == "Events":
                    site_awards.append(award)
                elif award['AwardType'] == "Game Beaten":
                    beaten_games.append(award)
                elif award['AwardType'] == "Mastery/Completion":
                    mastery_games.append(award)
                elif award['AwardType'] == "Patreon Supporter":
                    award['ImageIcon'] = "https://static.retroachievements.org/assets/images/badge/patreon.png"
                    site_awards.append(award)
                    
            await create_awards_mosaics(message, mastery_games, beaten_games, site_awards, ra_username)
        
    else:
        await message.channel.send("Não foi possível buscar seus troféus no momento. Tente novamente mais tarde.")    
    
async def create_awards_mosaics(message, mastery_games, beaten_games, site_awards, username):
    
    # Definindo tamanho do mosaico
    tile_size = 100         # Tamanho de cada ícone
    columns = 5             # Número fixo de colunas no mosaico
    gold_border_size = 5    # Tamanho da borda dourada para prêmios hardcore (maestria)
    silver_border_size = 5  # Tamanho da borda prateada para prêmios hardcore (jogos batidos)
    spacing = 5             # Espaçamento entre os badges
    extra_margin = 10       # Margem extra para evitar cortes

    # Função para criar e enviar o mosaico
    async def create_and_send_mosaic(awards, title, is_mastery):
        if not awards:
            return  # Não cria mosaico se a lista estiver vazia
        
        # Calculando altura e largura do mosaico considerando bordas e espaçamento
        rows = (len(awards) + columns - 1) // columns
        mosaic_width = (tile_size + 2 * (gold_border_size if is_mastery else silver_border_size)) * columns + spacing * (columns - 1)
        mosaic_height = (tile_size + 2 * (gold_border_size if is_mastery else silver_border_size)) * rows + spacing * (rows - 1) + extra_margin
        mosaic = Image.new('RGB', (mosaic_width, mosaic_height), (30, 30, 30))

        # Função para adicionar uma imagem ao mosaico com borda condicional
        def add_image_to_mosaic(image_url, x, y, is_hardcore):
            try:
                response = requests.get(image_url)
                response.raise_for_status()  # Levanta um erro se a requisição falhar
                img = Image.open(BytesIO(response.content)).resize((tile_size, tile_size))

                # Se for hardcore e for maestria, adiciona borda dourada
                if is_mastery and is_hardcore:
                    bordered_img = Image.new('RGB', (tile_size + 2 * gold_border_size, tile_size + 2 * gold_border_size), (255, 215, 0))  # Cor dourada
                    bordered_img.paste(img, (gold_border_size, gold_border_size))  # Coloca a imagem com a borda dourada
                    mosaic.paste(bordered_img, (x * (tile_size + spacing) + spacing, y * (tile_size + spacing) + spacing))
                # Se for hardcore e for jogos batidos, adiciona borda prateada
                elif not is_mastery and is_hardcore:
                    bordered_img = Image.new('RGB', (tile_size + 2 * silver_border_size, tile_size + 2 * silver_border_size), (192, 192, 192))  # Cor prateada
                    bordered_img.paste(img, (silver_border_size, silver_border_size))  # Coloca a imagem com a borda prateada
                    mosaic.paste(bordered_img, (x * (tile_size + spacing) + spacing, y * (tile_size + spacing) + spacing))
                else:
                    # Sem borda
                    mosaic.paste(img, ((x * (tile_size + spacing)) + spacing, (y * (tile_size + spacing)) + spacing))

            except Exception as e:
                print(f"Erro ao buscar ou processar a imagem: {e}")  # Log do erro

        # Adicionando as imagens ao mosaico
        for i, award in enumerate(awards):
            if award['ImageIcon'] is not None:
                x = i % columns
                y = i // columns
                is_hardcore = award.get('AwardDataExtra') == 1  # Verifica se é hardcore
                badge = award['ImageIcon'] if award['AwardType'] == "Patreon Supporter" else f"https://retroachievements.org{award['ImageIcon']}" # Verifica se o Badge é do Patreon (pois o link é diferente)
                add_image_to_mosaic(badge, x, y, is_hardcore)

        # Salvando e enviando o mosaico
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            mosaic.save(temp_file.name)
            await message.channel.send(f"`{username}` Aqui está o seu mosaico de - {title}:", file=discord.File(temp_file.name))

    # Criar e enviar mosaico para cada categoria
    await create_and_send_mosaic(mastery_games, "Jogos Masterizados", True)
    await create_and_send_mosaic(beaten_games, "Jogos Zerados", False)
    await create_and_send_mosaic(site_awards, "Badges do Site/Eventos", False)

async def send_registration_prompt(message):
    await message.channel.send("Você ainda não registrou seu usuário. Use o comando `!registrar <seu_usuario>` para registrar.")
