import os
from aiogram import Router, F
from aiogram.types import Message, PhotoSize
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.generators import ask_gemini
from io import BytesIO


router = Router()


class Generate(StatesGroup):
    text = State()
    image = State()


class AIState(StatesGroup):
    active = State()

# Activate AI mode
@router.message(Command("ai"))
async def cmd_ai(message: Message, state: FSMContext):
    await state.set_state(AIState.active)
    await message.answer("🤖 AI режим активирован! Отправьте текст или фото.")

# Deactivate AI mode
@router.message(Command("exit"))
async def cmd_exit(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ AI режим отключен. Используйте /ai для повторного включения.")

# Recognize AI text 
@router.message(AIState.active, F.text)
async def handle_ai_text(message: Message):
    response = await ask_gemini(message.text)
    await message.answer(response)

# Recognize AI photo
@router.message(AIState.active, F.photo)
async def handle_ai_photo(message: Message, state: FSMContext):
    photo: PhotoSize = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)
    file_path = file_info.file_path
    save_path = f"downloads/{photo.file_id}.jpg"

    await message.bot.download_file(file_path, save_path)

    user_text = message.caption if message.caption else ""

    response = await ask_gemini(user_text, image_path=save_path)
    await message.answer(response)

    os.remove(save_path)

    # await state.clear()

# Unknown AI
@router.message(AIState.active)
async def handle_unknown(message: Message):
    await message.answer("⚠️ Отправьте текст или фото!")


@router.message()
async def handle_other_comands(message: Message):
    await message.answer("⚡ Бот работает! Используйте команду /ai для общения с AI.")

# @router.message(CommandStart())
# async def cmd_start(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer("Botga hush kelibsiz")


# @router.message(F.text)
# async def generate(message: Message, state: FSMContext):
#     await state.set_state(Generate.text)
#     response = await ask_gemini(message.text)
#     await message.answer(response.choices[0].message.content)
#     await state.clear()


# @router.message(F.photo)
# async def generate_image(message: Message, state: FSMContext):
#     await state.set_state(Generate.image)

#     photo: PhotoSize = message.photo[-1]
#     photo_bytes = await photo.download(destination=BytesIO())
#     photo_bytes.seek(0)

#     response = await ask_gemini(image_path=photo_bytes)

# @router.message(Generate.text)
# async def generate_error(message: Message):
#     await message.answer("⏳ Подождите, бот уже обрабатывает ваше сообщение...")
