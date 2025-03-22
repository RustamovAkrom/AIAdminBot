import asyncio
import logging
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

from apps.bot.handlers import register_all_handlers
from apps.bot.utils import set_bot_commands

from apps.bot.utils import run_bot


async def main() -> None:
    bot, dp = run_bot()

    register_all_handlers(dp)

    await set_bot_commands(bot)

    try:
        logging.info("Бот запущен!")
        await dp.start_polling(bot)
    except Exception as e:
        logging.exception(f"Ошибка в работе бота: {e}")
    finally:
        await bot.session.close()
        logging.info("Бот остановлен!")


class Command(BaseCommand):
    help = "Run Telegram Bot"

    def handle(self, *args, **options):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            stream=sys.stdout,
        )

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            logging.info("Бот принудительно остановлен пользователем.")
        except Exception as e:
            logging.exception(f"Необработанная ошибка: {e}")
        finally:
            logging.info("Программа завершена.")
