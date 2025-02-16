from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="ai", description="🤖 Активировать AI"),
        BotCommand(command="exit", description="❌ Отключить AI"),
        BotCommand(command="help", description="ℹ️ Помощь"),
        BotCommand(command="about", description="📌 О проекте"),
    ]
    await bot.set_my_commands(commands)
