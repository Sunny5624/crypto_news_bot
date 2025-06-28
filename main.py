import os
import asyncio
import logging
from datetime import datetime, timedelta
from news_sources import fetch_watcher_guru_news, fetch_other_sites_news
from telegram_bot import send_telegram_message, send_daily_digest
from keep_alive import keep_alive

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

posted_urls = set()

async def main():
    keep_alive()

    async def watcher_task():
        while True:
            try:
                logger.info("Checking WatcherGuru...")
                news_items = fetch_watcher_guru_news()
                for title, url in news_items:
                    if url not in posted_urls:
                        await send_telegram_message(f"📰 <b>{title}</b>
{url}")
                        posted_urls.add(url)
                await asyncio.sleep(300)
            except Exception as e:
                logger.error(f"Watcher task error: {e}")

    async def other_sites_task():
        while True:
            try:
                logger.info("Checking other sites...")
                news_items = fetch_other_sites_news()
                for title, url in news_items:
                    if url not in posted_urls:
                        await send_telegram_message(f"🗞️ <b>{title}</b>
{url}")
                        posted_urls.add(url)
                await asyncio.sleep(1800)
            except Exception as e:
                logger.error(f"Other sites task error: {e}")

    async def daily_digest_task():
        while True:
            now = datetime.now()
            target_time = now.replace(hour=22, minute=0, second=0, microsecond=0)
            if now >= target_time:
                target_time += timedelta(days=1)
            wait_time = (target_time - now).total_seconds()
            await asyncio.sleep(wait_time)
            await send_daily_digest(posted_urls)

    await asyncio.gather(watcher_task(), other_sites_task(), daily_digest_task())

if __name__ == "__main__":
    asyncio.run(main())