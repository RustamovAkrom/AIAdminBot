from .base import APIClient


class PaymentService(APIClient):
    def create_payment(self, telegram_id, amount, currency, status):
        data = {
            "telegram_id": telegram_id,
            "amount": amount,
            "currency": currency,
            "status": status
        }
        self._request("POST", "bot/payments/", data)
