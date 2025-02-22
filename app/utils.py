from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands


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
