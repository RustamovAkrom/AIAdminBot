import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.handlers import ai_router, base_router
from app.utils import set_bot_commands


async def main() -> None:
    load_dotenv()

    bot = Bot(
        token=str(os.getenv("TG_TOKEN")),
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()

    dp.include_router(base_router)
    dp.include_router(ai_router)
    
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot disabled")
