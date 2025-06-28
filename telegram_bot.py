import os
from telegram import Bot
from telegram.constants import ParseMode

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(text):
    if TELEGRAM_TOKEN and CHAT_ID:
        await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)

async def send_daily_digest(posted_urls):
    message = "<b>📢 Daily Digest - Top Headlines</b>\n"
    for idx, url in enumerate(list(posted_urls)[-10:], start=1):
        message += f"{idx}. <a href='{url}'>Click here</a>\n"
    await send_telegram_message(message)