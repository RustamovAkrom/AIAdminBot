import os
import asyncio
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()

from apps.bot.utils import get_jwt_token
import requests

def main():
    url = "http://127.0.0.1:8000/api/v1/bot/telegram_users/"
    data = {
        "telegram_id": 124,
        "full_name": "Akromjon",
        "username": "@Akromjon",
    }
    response = requests.post(url, json=data)
    print(response.status_code)
    # print(await get_jwt_token("Akromjon", "2007"))
          
if __name__=='__main__':
    main()
