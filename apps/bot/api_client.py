import aiohttp
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class BaseAPI:
    """Базовый класс для работы с API (общие методы)"""

    def __init__(self, client: "APIClient", endpoint: str):
        self.client = client
        self.endpoint = endpoint

    async def _request(
        self, method: str, path: str = "", data: Optional[Dict[str, Any]] = None
    ):
        """Универсальный метод запроса"""
        url = f"{self.client.base_url}{self.endpoint}{path}"
        async with aiohttp.ClientSession(headers=self.client.headers) as session:
            async with session.request(method, url, json=data) as response:
                if response.status in (200, 201):
                    return await response.json()
                logger.error(f"API Error {response.status}: {await response.text()}")
                return None


class UserAPI(BaseAPI):
    """API для работы с пользователями"""

    def __init__(self, client: "APIClient"):
        super().__init__(client, "bot/telegram_users")

    async def get_user(self, telegram_id: int):
        return await self._request("GET", f"/{telegram_id}/")

    async def create_user(self, telegram_id: int, full_name: str, username: str):
        data = {
            "telegram_id": telegram_id,
            "full_name": full_name,
            "username": username,
        }
        return await self._request("POST", "/", data)

    async def update_user(self, telegram_id: int, data: Dict[str, Any]):
        return await self._request("PATCH", f"/{telegram_id}/", data)

    async def delete_user(self, telegram_id: int):
        return await self._request("DELETE", f"/{telegram_id}/")

    async def check_access(self, telegram_id: int) -> bool:
        user = await self.get_user(telegram_id)
        return user.get("is_active", False) if user else False


class AIChatAPI(BaseAPI):
    """API для работы с AI-чатом"""

    def __init__(self, client: "APIClient"):
        super().__init__(client, "bot/ai_chat_history")

    async def get_chat_history(self, user_id: int):
        return await self._request("GET", f"/{user_id}/")

    async def save_message(self, user_id: int, message: str, response: str):
        data = {"user_id": user_id, "message": message, "response": response}
        return await self._request("POST", "/", data)


class PaymentAPI(BaseAPI):
    """API для управления платежами"""

    def __init__(self, client: "APIClient"):
        super().__init__(client, "bot/payments")

    async def create_payment(self, user_id: int, amount: float):
        data = {"user_id": user_id, "amount": amount}
        return await self._request("POST", "/", data)

    async def get_payment_status(self, payment_id: int):
        return await self._request("GET", f"/{payment_id}/")


class APIClient:
    """Основной клиент API (агрегатор всех API)"""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # Подключаем API-модули
        self.users = UserAPI(self)
        self.ai_chat = AIChatAPI(self)
        self.payments = PaymentAPI(self)
