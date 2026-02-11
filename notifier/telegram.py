import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from telegram import Bot
from config_pkg.setting import TELEGRAM_TOKEN, TELEGRAM_CHANNEL_ID

bot = Bot(token=TELEGRAM_TOKEN)

async def send_async(message: str):
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID, 
            text=message,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        return True
    except Exception as e:
        print(f"! Telegram error: {e}")
        return False

def send(message: str):
    try:
        return asyncio.run(send_async(message))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(send_async(message))