from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Salom butga hush kelibsiz {message.from_user.full_name}")


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
    profile_text = (
        f"👤 *Ваш профиль*\n"
        f"👥 Имя: `{user.full_name}`\n"
        f"🆔 ID: `{user.id}`\n"
        f"📅 Дата регистрации: _заполнить из БД_\n"
        f"💰 Баланс: _заполнить из БД_\n"
        f"⭐ Статус: _Обычный пользователь или Суперпользователь_"
    )
    await message.answer(profile_text, parse_mode="Markdown")


@router.message(Command("connect"))
async def connect(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📩 Связаться в Telegram", url="https://t.me/AkromRustamov2007"
                )
            ]
        ]
    )
    await message.answer(
        "💬 Если у вас есть вопросы или предложения, свяжитесь со мной:",
        reply_markup=keyboard,
    )
