from app.generators import ask_gemini
import asyncio
async def output():
    # while True:
    output = await ask_gemini(input(""), image_path="image.png")
    print(f"AI: ", output)

asyncio.run(output())
from whisper import load_model