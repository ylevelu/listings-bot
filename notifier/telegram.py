from telegram import Bot
from telegram import __version__ as ptb_version
import asyncio
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_async(ann):
    emoji = "🟢" if ann.category == "listing" else "🔴"
    text = (
        f"{emoji} {ann.exchange}\n"
        f"{ann.category.upper()} | {ann.market_type.upper()}\n\n"
        f"{ann.title}\n\n"
        f"{ann.url}"
    )
    await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=text)

def send(ann):
    asyncio.run(send_async(ann))
