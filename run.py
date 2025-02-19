import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.handlers import ai_router, base_router, payment_router
from app.utils import set_bot_commands, set_bot_commands_for_language


async def main() -> None:
    load_dotenv()

    bot = Bot(
        token=str(os.getenv("TG_TOKEN")),
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()

    dp.include_router(base_router)
    dp.include_router(ai_router)
    dp.include_router(payment_router)
    
    bot_info = await bot.get_me()
    language_code = bot_info.language_code if bot_info.language_code else "ru"

    if language_code in ["en", "ru"]:
        await set_bot_commands_for_language(bot, language_code)
    else:
        await set_bot_commands(bot)

    try:
        logging.info("Бот запущен!")
        await dp.start_polling(bot)
    except Exception as e:
        logging.exception(f"Ошибка в работе бота: {e}")
    finally:
        await bot.session.close()
        logging.info("Бот остановлен!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", stream=sys.stdout)

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
