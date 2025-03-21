from .base import APIClient


class UsersService(APIClient):
    def get_user(self, telegram_id):
        return self._request("GET", f"bot/telegram_users/{telegram_id}")
    
    def create_user(self, data):
        return self._request("POST", "bot/telegram_users/", data)
