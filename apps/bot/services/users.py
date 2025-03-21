import requests
from core import settings


BASE_URL = settings.API_BASE_URL


def create_user(data):
    """ Create user through API """
    try:
        response = requests.post(f"{BASE_URL}bot/telegram_users/", json=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return None, {"error": e}
    

def get_user(telegram_id):
    try:
        resposne = requests.get(f"{BASE_URL}/{telegram_id}")
        resposne.raise_for_status()
        return resposne.status_code, resposne.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None, {"error": e}
