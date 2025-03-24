import logging

from django.conf import settings

from apps.bot.utils import get_jwt_token

import requests


class APIClient:

    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.tokens = self.get_tokens()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokens.get('access')}",
        }

    def get_tokens(self):
        tokens = get_jwt_token(settings.USERNAME, settings.PASSWORD)
        if not tokens.get("access"):
            raise Exception("Не удалось получить токен. Проверь логин и пароль.")
        return tokens

    def refresh_token(self):
        refresh_token = self.tokens.get('refresh')
        if not refresh_token:
            print("❌ Отсутствует refresh токен, получаю новые токены!")
            self.tokens = self.get_tokens()
            self.headers['Authorization'] = f"Bearer {self.tokens['access']}"
            return
        
        response = requests.post(
            f"{self.base_url}/api/v1/token/refresh",
            json={"refresh": refresh_token},
        )
        if response.status_code == 200:
            self.tokens['access'] = response.json().get("access")
            self.headers['Authorization'] = f"Bearer {self.tokens['access']}"
            print("🔄 Токен успешно обновлён!")
        else:
            print("❌ Не удалось обновить токен, получаю новые токены!")
            self.tokens = self.get_tokens()
            self.headers["Authorization"] = f"Bearer {self.tokens['access']}"

    def _request(self, method, endpoint, data=None, retries=1):

        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.request(
                method=method, url=url, json=data, headers=self.headers
            )
            if response.status_code == 401 and retries > 0:
                print("⚠️ Токен истёк. Пробую обновить!")
                # self.refresh_token()
                return self._request(method, endpoint, data, retries=retries - 1)

            try:
                data = response.json()
            except Exception:
                data = None

            return response.status_code, data
        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
            return None, {"error": str(e)}
