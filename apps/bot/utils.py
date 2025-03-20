from django.conf import settings

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands

from core import settings


async def get_jwt_token(username: str, password: str):
    url = f"{settings.API_BASE_URL}/token/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"username": username, "password": password}) as response:
            if response.status == 200:
                return await response.json()
            else:
                text = await response.json()
                raise Exception(f"Ошибка {response.status}: {text}")



async def set_bot_commands(bot: Bot):
    """Устанавливает команды бота и интегрирует их с меню Telegram"""
    commands = [
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="ai", description="🤖 Активировать AI"),
        BotCommand(command="exit", description="❌ Отключить AI"),
        BotCommand(command="donate", description="💰 Поддержать проект"),
        BotCommand(command="help", description="ℹ️ Помощь"),
        BotCommand(command="about", description="📌 О проекте"),
    ]

    # Устанавливаем команды глобально для всех пользователей
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

    # Добавляем кнопки в главное меню Telegram
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())


def run_bot() -> tuple[Bot, Dispatcher]:
    bot = Bot(
        token=str(settings.TELEGRAM_TOKEN),
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    dp = Dispatcher()
    return bot, dp
