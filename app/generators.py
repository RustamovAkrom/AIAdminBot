import google.generativeai as genai
import os
import asyncio
from dotenv import load_dotenv
from collections import deque, defaultdict
from PIL import Image
import mimetypes
import io


load_dotenv()

GOOGLE_API_KEY = os.getenv("AI_TOKEN")

AI_CONFIG = {
    "model": "gemini-1.5-flash",
    "temperature": 0.7,
    "max_tokens": 500,
    "role": "Ты полезный ассистент, который отвечает кратко и по делу."
}

if not GOOGLE_API_KEY:
    raise ValueError("❌ API-ключ не найден! Проверь .env файл.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(AI_CONFIG['model'])

user_chat_history = defaultdict(lambda: deque(maxlen=10))


async def process_file(file_path: str):
    mime_type, _ = mimetypes.guess_type(file_path)

    if not mime_type:
        return None, "❌ Неизвестный формат файла."
    
    elif mime_type.startswith("image"): # Photo
        return Image.open(file_path), None
    
    # elif mime_type.startswith("audio"): # Audio
    #     return open(file_path, "rb"), None
    
    # elif mime_type.startswith("video"): # Video
    #     return open(file_path, "rb"), None
    
    elif mime_type in ["text/plain", "application/pdf", "text/csv"]: # Text files
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                text = f.read()
            return text, None
        except Exception:
            return None, "❌ Ошибка при чтении файла."

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
            messages[-1]['parts'].append(file_data)
        
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
