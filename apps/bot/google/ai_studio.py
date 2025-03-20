import os
import aiofiles
import asyncio
from django.conf import settings
import google.generativeai as genai
from collections import deque, defaultdict
from PIL import Image
import mimetypes


MAX_FILE_SIZE = 10 * 1024 * 1024


AI_CONFIG = {
    "model": "gemini-1.5-flash",
    "temperature": 0.7,
    "max_tokens": 500,
    "role": "Ты полезный ассистент, который отвечает кратко и по делу.",
}

if not settings.GOOGLE_AI_TOKEN:
    raise ValueError("❌ API-ключ не найден! Проверь .env файл.")


genai.configure(api_key=settings.GOOGLE_AI_TOKEN)
model = genai.GenerativeModel(AI_CONFIG["model"])

user_chat_history = defaultdict(lambda: deque(maxlen=10))


async def process_image(file_path: str):
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        return None, "❌ Файл слишком большой."

    try:
        return Image.open(file_path), None
    except Exception:
        return None, "❌ Ошибка при обработке изображения."


async def process_text(file_path: str):
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            text = await f.read()
        return text, None
    except Exception:
        return None, "❌ Ошибка при чтении файла."


async def process_file(file_path: str):
    mime_type, _ = mimetypes.guess_type(file_path)

    if not mime_type:
        return None, "❌ Неизвестный формат файла."

    if mime_type.startswith("image"):
        return await process_image(file_path)

    if mime_type in ["text/plain", "application/pdf", "text/csv"]:  # Text files
        return await process_text(file_path)

    else:
        return None, f"❌ Формат {mime_type} не поддерживается."


async def ask_gemini(user_id: int, prompt: str, file_path: str = None) -> str:
    try:
        messages = list(user_chat_history[user_id])
        messages.append({"role": "user", "parts": [prompt]})

        if file_path:
            file_data, error = await process_file(file_path)

            if error:
                return error
            messages[-1]["parts"].append(file_data)

        response = await asyncio.to_thread(model.generate_content, messages)

        if response and hasattr(response, "text"):
            ai_response = response.text
            user_chat_history[user_id].append({"role": "user", "parts": [prompt]})
            user_chat_history[user_id].append({"role": "model", "parts": [ai_response]})
            return ai_response

        else:
            return "❌ Ответ от AI пуст или был заблокирован."

    except Exception as e:
        return f"❌ Ошибка AI: {e}"
