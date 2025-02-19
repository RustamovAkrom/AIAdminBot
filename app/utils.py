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


async def set_bot_commands_for_language(bot: Bot, language_code: str):
    """Устанавливает команды для конкретного языка"""
    localized_commands = {
        "en": [
            BotCommand(command="start", description="🚀 Start bot"),
            BotCommand(command="ai", description="🤖 Activate AI"),
            BotCommand(command="exit", description="❌ Disable AI"),
            BotCommand(command="donate", description="💰 Support project"),
            BotCommand(command="help", description="ℹ️ Help"),
            BotCommand(command="about", description="📌 About the project"),
        ],
        "ru": [
            BotCommand(command="start", description="🚀 Запустить бота"),
            BotCommand(command="ai", description="🤖 Активировать AI"),
            BotCommand(command="exit", description="❌ Отключить AI"),
            BotCommand(command="donate", description="💰 Поддержать проект"),
            BotCommand(command="help", description="ℹ️ Помощь"),
            BotCommand(command="about", description="📌 О проекте"),
        ],
    }

    if language_code in localized_commands:
        await bot.set_my_commands(localized_commands[language_code], scope=BotCommandScopeDefault())

