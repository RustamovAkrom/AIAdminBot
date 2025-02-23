import os
import asyncio
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()

from apps.bot.utils import get_jwt_token


async def main():
    print(await get_jwt_token("Akromjon", "2007"))
          
if __name__=='__main__':
    asyncio.run(main())