import os
import asyncio
import logging
from datetime import datetime, timedelta
from news_sources import fetch_watcher_guru_news, fetch_other_sites_news
from telegram_bot import send_telegram_message, send_daily_digest
from keep_alive import keep_alive

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Posted URLs tracker
posted_urls = set()

# Main Async Function
async def main():
    keep_alive()
    logger.info("✅ Bot started and keep_alive running...")

    # WatcherGuru Task
    async def watcher_task():
        while True:
            try:
                logger.info("📡 Checking WatcherGuru...")
                news_items = await fetch_watcher_guru_news()
                logger.info(f"📰 Found {len(news_items)} news items from WatcherGuru")

                for title, url in news_items:
                    if url not in posted_urls:
                        logger.info(f"📤 Sending: {title}")
                        await send_telegram_message(f"📰 <b>{title}</b>\n<a href=\"{url}\">Read More</a>")
                        posted_urls.add(url)
                await asyncio.sleep(300)  # Wait 5 minutes
            except Exception as e:
                logger.error(f"❌ Watcher task error: {e}")

    # Other Sites Task
    async def other_sites_task():
        while True:
            try:
                logger.info("📡 Checking other sites...")
                news_items = await fetch_other_sites_news()
                logger.info(f"🗞️ Found {len(news_items)} news from other sources")

                for title, url in news_items:
                    if url not in posted_urls:
                        logger.info(f"📤 Sending: {title}")
                        await send_telegram_message(f"🗞️ <b>{title}</b>\n<a href=\"{url}\">Read More</a>")
                        posted_urls.add(url)
                await asyncio.sleep(1800)  # Wait 30 minutes
            except Exception as e:
                logger.error(f"❌ Other sites task error: {e}")

    # Daily Digest Task
    async def daily_digest_task():
        while True:
            now = datetime.now()
            target_time = now.replace(hour=22, minute=0, second=0, microsecond=0)
            if now >= target_time:
                target_time += timedelta(days=1)
            wait_time = (target_time - now).total_seconds()

            logger.info(f"🕒 Waiting for daily digest time: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
            await asyncio.sleep(wait_time)

            logger.info("📨 Sending daily digest...")
            await send_daily_digest(posted_urls)

            # Optional: Clear old posts after digest
            # posted_urls.clear()

    # Run All Tasks
    try:
        await asyncio.gather(
            watcher_task(),
            other_sites_task(),
            daily_digest_task()
        )
    except Exception as e:
        logger.error(f"💥 Main loop error: {e}")

# Entry Point
if __name__ == "__main__":
    asyncio.run(main())

