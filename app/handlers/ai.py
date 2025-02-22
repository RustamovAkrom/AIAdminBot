import os
import openai
from aiogram import Router, F, Bot
from aiogram.types import Message, PhotoSize, Video, Document
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.generators import ask_gemini
from dotenv import load_dotenv

load_dotenv()
router = Router()

openai.api_key = os.getenv("OPENAI_API_KEY")


class AIState(StatesGroup):
    active = State()


# Activate AI mode
@router.message(Command("ai"))
async def cmd_ai(message: Message, state: FSMContext):
    await state.set_state(AIState.active)
    await message.answer("🤖 AI режим активирован! Отправьте текст или фото.")
    await message.answer("Для отключения AI-режима введите команду /exit.")


# Deactivate AI mode
@router.message(Command("exit"))
async def cmd_exit(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❌ AI режим отключен. Используйте /ai для повторного включения."
    )


# Recognize AI text
@router.message(AIState.active, F.text)
async def handle_ai_text(message: Message, bot: Bot):
    user_id = message.from_user.id

    processing_msg = await message.answer(
        "⏳ Пожалуйста, подождите, ваш запрос обрабатывается..."
    )
    response = await ask_gemini(user_id, message.text)
    await bot.send_chat_action(message.chat.id, "typing")
    await processing_msg.delete()
    await message.answer(response)


# Recognize AI photo
@router.message(AIState.active, F.photo)
async def handle_ai_photo(message: Message, bot: Bot):
    user_id = message.from_user.id

    photo: PhotoSize = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)
    file_path = file_info.file_path
    save_path = f"downloads/{photo.file_id}.jpg"

    processing_msg = await message.answer(
        "Пожалуйста, подождите, бот обрабатывает ваш файл..."
    )

    await message.bot.download_file(file_path, save_path)

    user_text = message.caption if message.caption else ""

    response = await ask_gemini(user_id, user_text, file_path=save_path)

    await bot.send_chat_action(message.chat.id, "typing")
    await processing_msg.delete()
    await message.answer(response)

    os.remove(save_path)


# Recognize AI photo
@router.message(AIState.active, F.video)
async def handle_ai_photo(message: Message, bot: Bot):
    user_id = message.from_user.id

    video: Video = message.video
    file_info = await message.bot.get_file(video.file_id)
    file_path = file_info.file_path
    save_path = f"downloads/{video.file_id}.mp4"

    processing_msg = await message.answer(
        "Пожалуйста, подождите, бот обрабатывает ваш файл..."
    )

    await message.bot.download_file(file_path, save_path)

    user_text = message.caption if message.caption else ""

    response = await ask_gemini(user_id, user_text, file_path=save_path)

    await bot.send_chat_action(message.chat.id, "typing")
    await processing_msg.delete()
    await message.answer(response)

    os.remove(save_path)


# Recognize AI document
@router.message(AIState.active, F.document)
async def handle_ai_video(message: Message, bot: Bot):
    user_id = message.from_user.id

    video: Document = message.document
    file_info = await message.bot.get_file(video.file_id)
    file_path = file_info.file_path
    save_path = f"downloads/{video.file_name}"

    processing_msg = await message.answer(
        "⏳ Пожалуйста, подождите, бот обрабатывает ваш файл..."
    )

    await message.bot.download_file(file_path, save_path)

    user_text = message.caption if message.caption else "Проанализируй этот файл."

    response = await ask_gemini(user_id, user_text, file_path=save_path)

    await bot.send_chat_action(message.chat.id, "typing")
    await processing_msg.delete()
    await message.answer(response)

    os.remove(save_path)


# Unknown AI
@router.message(AIState.active)
async def handle_unknown(message: Message):
    await message.answer("⚠️ Отправьте текст или фото!")
