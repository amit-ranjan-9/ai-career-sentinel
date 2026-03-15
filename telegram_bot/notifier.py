import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_message_async(text: str):
    bot = Bot(token=BOT_TOKEN)
    # Split into chunks if too long
    max_length = 4000
    chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    for chunk in chunks:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=chunk
            # No parse_mode — plain text, no markdown issues
        )

def send_telegram_brief(text: str):
    print("[Telegram] Sending morning brief...")
    asyncio.run(send_message_async(text))
    print("[Telegram] Brief sent successfully! ✅")