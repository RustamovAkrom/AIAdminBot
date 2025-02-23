from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup


router = Router()


@router.message(Command("open_web_app"))
async def open_web_app(message: types.Message):
    keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Open Web App",
                    web_app=WebAppInfo(url="https://github.com/RustamovAkrom"),
                )
            ]
        ]
    )
    await message.answer("GitHub Rustamov Akrom", reply_markup=keyboard_markup)
