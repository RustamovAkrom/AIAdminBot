import os
import re

import openai
from aiogram import Router, F, Bot
from aiogram.types import Message, PhotoSize, Video, Document
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from apps.bot.google.ai_studio import ask_gemini
from dotenv import load_dotenv


load_dotenv()
router = Router()

openai.api_key = os.getenv("OPENAI_API_KEY")


class AIState(StatesGroup):
    active = State()


def escape_markdown(text):
    """
    Экранирует текст под Telegram MarkdownV2, чтобы не сломался формат.
    """
    escape_chars = r"_*[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


async def send_ai_response(bot, chat_id, text):
    """
    Отправляет AI-ответ с обработкой Markdown и делением на части.
    """
    text = escape_markdown(text)

    # Делим текст на части по 4096 символов (лимит Telegram)
    chunks = [text[i:i + 4096] for i in range(0, len(text), 4096)]

    for chunk in chunks:
        try:
            # Пробуем отправить с MarkdownV2
            await bot.send_message(chat_id=chat_id, text=chunk, parse_mode="MarkdownV2")
        except Exception as e:
            print(f"⚠️ Ошибка отправки Markdown: {e}")
            try:
                # Если Markdown сломался — шлём обычный текст
                await bot.send_message(chat_id=chat_id, text=chunk)
            except Exception as e:
                print(f"❌ Критическая ошибка отправки: {e}")

# Activate AI mode
@router.message(Command("ai"))
async def cmd_ai(message: Message, state: FSMContext):
    await state.set_state(AIState.active)
    await message.answer(
        "🤖 AI режим активирован! Отправьте текст или фото.\n"
        "Для отключения AI-режима введите команду /exit.\n"
    )


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

    await processing_msg.delete()
    
    MAX_LENGTH = 4096
    for chunk in [response[i: i + MAX_LENGTH] for i in range(0, len(response), MAX_LENGTH)]:
        await bot.send_chat_action(message.chat.id, "typing")
        # await message.answer(escape_markdown(chunk))
        await send_ai_response(message.bot, message.chat.id, chunk)


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

    await processing_msg.delete()

    MAX_LENGTH = 4096
    for chunk in [response[i: i + MAX_LENGTH] for i in range(0, len(response), MAX_LENGTH)]:
        await bot.send_chat_action(message.chat.id, "typing")
        await message.answer(chunk)

    os.remove(save_path)


# Recognize AI document
@router.message(AIState.active, F.document)
async def handle_ai_document(message: Message, bot: Bot):
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

    await processing_msg.delete()

    MAX_LENGTH = 4096
    for chunk in [response[i: i + MAX_LENGTH] for i in range(0, len(response), MAX_LENGTH)]:
        await bot.send_chat_action(message.chat.id, "typing")
        await message.answer(chunk)

    os.remove(save_path)


# Unknown AI
@router.message(AIState.active)
async def handle_unknown(message: Message):
    await message.answer("⚠️ Отправьте текст или фото!")