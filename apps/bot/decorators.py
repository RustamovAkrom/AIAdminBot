from core import settings
from apps.bot.utils import run_bot
from apps.bot.services import users
from aiogram import types
import traceback
import functools


api = users.UsersService()


def error_handler(func):
    bot, _ = run_bot()

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(
                *args,
                **{k: v for k, v in kwargs.items() if k in func.__code__.co_varnames},
            )
        except Exception:
            message = next(
                (arg for arg in args if isinstance(arg, types.Message)), None
            )

            error_text = f"🚨 Произошла ошибка:\n\n`{traceback.format_exc()}`"
            print(error_text)

            if message:
                await message.answer("⚠️ Произошла ошибка! Мы уже работаем над этим.")

            await bot.send_message(settings.TELEGRAM_ADMIN_ID, error_text)

    return wrapper
