import requests


BASE_URL = "http://127.0.0.1:8000/api/v1/bot/telegram_users"


def create_user(data):
    """ Create user through API """
    try:
        response = requests.post(BASE_URL, json=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return None
    

def get_user(telegram_id):
    try:
        resposne = requests.get(f"{BASE_URL}/{telegram_id}")
        resposne.raise_for_status()
        return resposne.status_code, resposne.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None
