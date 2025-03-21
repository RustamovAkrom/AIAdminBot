from core import settings
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from apps.bot.utils import run_bot
from apps.bot.services import users


router = Router()
api_users = users.UsersService()

OWNER_ID = settings.TELEGRAM_ADMIN_ID


@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    data = {
        "telegram_id": user.id,
        "full_name": user.full_name,
        "username": user.username,
    }

    status, user_data = api_users.create_user(data)

    if status is None:
        await message.answer(
            "⚠️ API bilan bog'lanishda muammo yuz berdi. Keyinroq urinib ko'ring."
        )

    await message.answer(
        f"👋 Salom, {user.full_name}! Qanday yordam berishim munkin?\n\n"
    )


@router.message(Command("help"))
async def help(message: Message):
    text = (
        "✅ /ai — 🤖 Активировать AI\n"
        "✅ /exit — ❌ Отключить AI\n"
        "✅ /help — ℹ️ Помощь\n"
        "✅ /about — 📌 О проекте\n"
        "✅ /connect — 📞 Связаться с тобой\n"
        "✅ /feedback — 💬 Оставить отзыв или задать вопрос\n"
        "✅ /profile — 🏠 Личный кабинет\n"
        "✅ /donate — 💰 Поддержать проект\n"
    )
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("about"))
async def about(message: Message):
    text = (
        "📌 *О проекте*\n\n"
        "Этот бот создан для помощи пользователям с AI, "
        "а также для удобного взаимодействия через Telegram.\n\n"
        "🔹 *Функционал:*\n"
        "— Интеграция с AI\n"
        "— Поддержка пользователей\n"
        "— Прием донатов\n"
        "— Расширенные возможности API\n\n"
        "💡 Разработка: *Akrom Rustamov*"
    )
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("profile"))
async def profile(message: Message):
    user = message.from_user
    chat = await message.bot.get_chat(user.id)

    # Собираем всю доступную информацию о пользователе
    profile_text = (
        f"👤 *Ваш профиль*\n"
        f"👥 Имя: `{user.full_name}`\n"
        f"🆔 ID: `{user.id}`\n"
        f"🔗 Username: `@{user.username if user.username else 'Не указан'}`\n"
        f"🌍 Язык: `{user.language_code}`\n"
        f"🛠️ Premium: `{'Да' if user.is_premium else 'Нет'}`\n"
        f"📱 Телефон: `{'Не доступен через Telegram API'}`\n"
        f"🔒 Приватность: `{'Да' if chat.has_private_forwards else 'Нет'}`\n"
        # f"✅ Верифицирован: `{'Да' if chat.is_verified else 'Нет'}`\n"
        f"🏷️ Bio: `{chat.bio if chat.bio else 'Не указано'}`\n"
        f"🔹 Тип чата: `{chat.type}`\n"
        f"`{chat.location}`"
        # f"👑 Статус администратора: `{'Да' if chat.is_creator else 'Нет'}`"
    )

    await message.answer(profile_text)


async def get_owner_username():
    bot, _ = run_bot()
    user_info = await bot.get_chat(OWNER_ID)
    return user_info.username


@router.message(Command("connect"))
async def connect(message: Message):
    username = await get_owner_username()

    if username:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📩 Связаться в Telegram", url=f"https://t.me/{username}"
                    )
                ]
            ]
        )

        await message.answer(
            "💬 Если у вас есть вопросы или предложения, свяжитесь со мной:",
            reply_markup=keyboard,
        )
    else:
        await message.answer("У владельца нет username 😅")
