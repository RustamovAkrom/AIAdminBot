import asyncio
import logging
import os
import sys

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.bot.handlers import register_all_handlers
from apps.bot.utils import set_bot_commands

async def run_bot() -> None:
    bot = Bot(
            token=str(settings.TELEGRAM_TOKEN),
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
        )
    dp = Dispatcher()
    
        
    register_all_handlers(dp)

    set_bot_commands(bot)
    
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
            loop.run_until_complete(run_bot())
        except KeyboardInterrupt:
            logging.info("Бот принудительно остановлен пользователем.")
        except Exception as e:
            logging.exception(f"Необработанная ошибка: {e}")
        finally:
            logging.info("Программа завершена.")
