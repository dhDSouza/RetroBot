import requests
import os
import random

RA_API_KEY = os.getenv('RA_API_KEY')

# Função para buscar as conquistas recentes via API do RetroAchievements
def get_recent_achievements(username):
    url = f"https://retroachievements.org/API/API_GetUserRecentAchievements.php?y={RA_API_KEY}&u={username}&m=1440"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Erro ao buscar conquistas: {e}")
        return None

# Função para obter todos os consoles disponíveis
def get_consoles():
    url = f"https://retroachievements.org/API/API_GetConsoleIDs.php?y={RA_API_KEY}&a=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Erro ao buscar consoles: {e}")
        return None

# Função para obter jogos de um console específico
def get_games_for_console(console_id):
    url = f"https://retroachievements.org/API/API_GetGameList.php?y={RA_API_KEY}&i={console_id}&f=1"
    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Erro ao buscar jogos: {e}")
        return None

# Função para sortear um console e um jogo daquele console
def get_random_challenge():
    
    consoles = get_consoles()
    if consoles:
        random_console = random.choice(consoles)
        console_id = random_console['ID']
        console_name = random_console['Name']
        console_image_url = random_console['IconURL']
        games = get_games_for_console(console_id)

        if games:
            random_game = random.choice(games)
            game_name = random_game['Title']
            game_id = random_game['ID']
            game_image_url = f"https://retroachievements.org{random_game['ImageIcon']}"
            
            return {
                "console": console_name,
                "game": game_name,
                "game_id": game_id,
                "game_image_url": game_image_url,
                "console_image_url": console_image_url
            }
        else:
            return None
    else:
        return None
    
# Função para consultar o progresso do jogador em um jogo
def fetch_player_progress(username, game_id):
    url = f"https://retroachievements.org/API/API_GetUserProgress.php?y={RA_API_KEY}&u={username}&i={game_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if str(game_id) in data:
            return data[str(game_id)]
        else:
            return None
        
    except Exception as e:
        print(f"Erro ao consultar progresso do jogador {username}: {e}")
        return None
    
# Função para buscar informações sobre o perfil do jogador
def fetch_user_profile(username):
    url = f'https://retroachievements.org/API/API_GetUserProfile.php?y={RA_API_KEY}&u={username}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Erro ao buscar informações do perfil: {e}")
        return None