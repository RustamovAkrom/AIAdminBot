from .base import APIClient
from .users import UsersService

api_users = UsersService()


class FeedbackService(APIClient):
    def create_feedback(self, telegram_id, message):
        data = {
            "telegram_id": telegram_id,
            "message": message
        }
        return self._request("POST", "bot/feedback/", data)
