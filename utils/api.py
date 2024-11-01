import requests
import os
import random

from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API do RetroAchievements do arquivo .env
RA_API_KEY = os.getenv('RA_API_KEY')

# Função genérica para chamadas à API
def call_ra_api(endpoint, params=None):
    base_url = "https://retroachievements.org/API/"
    params = params or {}
    
    # Adicionar a chave da API em todos os requests
    params['y'] = RA_API_KEY
    
    try:
        # Realiza a requisição HTTP para a API com os parâmetros
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        # Retorna o JSON da resposta, ou None se o status não for 200
        return response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        print(f"Erro ao fazer requisição para {endpoint}: {e}")
        return None

# Função para buscar as conquistas recentes de um usuário via API do RetroAchievements
def get_recent_achievements(username):
    endpoint = "API_GetUserRecentAchievements.php"
    params = {
        'u': username,
        'm': 1440  # Últimas 24 horas (em minutos)
    }
    return call_ra_api(endpoint, params)

# Função para obter todos os consoles disponíveis via API
def get_consoles():
    endpoint = "API_GetConsoleIDs.php"
    params = {
        'g': 1 # Apenas consoles de jogos (excluí Hubs e Eventos)
    }
    return call_ra_api(endpoint, params)

# Função para obter a lista de jogos de um console específico
def get_games_for_console(console_id):
    endpoint = "API_GetGameList.php"
    params = {
        'f': 1, # Apenas jogos com conquistas
        'i': console_id  # ID do console
    }
    return call_ra_api(endpoint, params)

# Função para sortear um console e um jogo daquele console
def get_random_challenge():
    consoles = get_consoles()
    
    if consoles:
        # Seleciona um console aleatório
        random_console = random.choice(consoles)
        console_id = random_console['ID']
        console_name = random_console['Name']
        console_image_url = random_console['IconURL']
        
        # Obtém a lista de jogos do console sorteado
        games = get_games_for_console(console_id)

        if games:
            # Seleciona um jogo aleatório desse console
            random_game = random.choice(games)
            game_name = random_game['Title']
            game_id = random_game['ID']
            game_image_url = f"https://retroachievements.org{random_game['ImageIcon']}"
            
            # Retorna as informações do desafio
            return {
                "console": console_name,
                "game": game_name,
                "game_id": game_id,
                "game_image_url": game_image_url,
                "console_image_url": console_image_url
            }
        else:
            print("Erro ao buscar jogos para o console.")
            return None
    else:
        print("Erro ao buscar consoles.")
        return None

# Função para consultar o progresso de um jogador em um jogo
def fetch_player_progress(username, game_id):
    endpoint = "API_GetUserProgress.php"
    params = {
        'u': username,
        'i': game_id
    }
    return call_ra_api(endpoint, params)

# Função para buscar informações do perfil de um jogador
def fetch_user_profile(username):
    endpoint = "API_GetUserProfile.php"
    params = {
        'u': username
    }
    return call_ra_api(endpoint, params)

# Função para consultar o último jogo jogado por um usuário
def get_last_game_played(username):
    endpoint = "API_GetUserRecentlyPlayedGames.php"
    params = {
        'u': username,
        'c': 1  # Pegando apenas o último jogo jogado
    }
    return call_ra_api(endpoint, params)

# Funçao para consultar as premições do jogador.
def get_awards(username):
    endpoint = "API_GetUserAwards.php"
    params = {
        'u': username
    }
    return call_ra_api(endpoint, params)