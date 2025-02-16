import os
from aiogram import Router, F
from aiogram.types import Message, PhotoSize
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Salom butga hush kelibsiz {message.from_user.full_name}")


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        f"/profile \\- *shahshiy kabinet*\n"
        f"/about \\- *malumotlarni bilish*\n"
        f"/ai \\- *Suniy intelektni aktivlashtirish*\n"
        f"/connect \\- *Men bilan boglanish*\n"
        f"/feedback \\- *Savol va maslahatlarni qoldirish*\n",
        parse_mode="MarkdownV2"
    )


@router.message(Command("about"))
async def about(message: Message):
    await message.answer("About ...")


@router.message(Command("profile"))
async def profile(message: Message):
    await message.answer("Profile ...")


@router.message(Command("feedback"))
async def feedback(message: Message):
    await message.answer("Feedback ...")


@router.message(Command("connect"))
async def connect(message: Message):
    await message.answer("Connect ...")
