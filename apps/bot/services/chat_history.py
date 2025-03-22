from .base import APIClient


class ChatHistoryService(APIClient):
    def create_history(self, telegram_id, message, response): ...
