import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()

from apps.bot.services.base import APIClient

client = APIClient()

client.headers['Authorization'] = "Bearer yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyODg1OTIzLCJpYXQiOjE3NDI3OTk1MjMsImp0aSI6IjY0ZmVmZTQ1NWJkNDQ1YTRhYjE5MWQyMWFiZWZlOTg3IiwidXNlcl9pZCI6Mn0.8y_cddyMeIRQUAd9UA91ZWKrmIEha1lVqtHssmq3V0E"

status, data = client._request("GET", "bot/telegram_users/4/")
print(status, data)