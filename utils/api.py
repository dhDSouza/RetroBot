import requests
import os

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
