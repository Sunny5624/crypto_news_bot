import aiohttp
from bs4 import BeautifulSoup
from pyppeteer import launch

async def fetch_watcher_guru_news():
    url = "https://watcher.guru"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                articles = soup.select("a.home-news-card")
                news_items = []
                for a in articles[:10]:
                    title = a.get("title") or a.get_text(strip=True)
                    href = a.get("href")
                    full_url = f"https://watcher.guru{href}" if href else ""
                    if title and full_url:
                        news_items.append((title, full_url))
                return news_items
    except Exception as e:
        print(f"Error fetching watcher.guru news: {e}")
        return []

async def fetch_other_sites_news():
    other_sites = {
        "CoinDesk": "https://www.coindesk.com",
        "Cointelegraph": "https://cointelegraph.com",
        "The Block": "https://www.theblock.co",
        "Decrypt": "https://decrypt.co",
        "Messari": "https://messari.io",
        "Coin Center": "https://www.coincenter.org",
        "CryptoPanic": "https://cryptopanic.com/news/",
        "Glassnode": "https://insights.glassnode.com",
        "Santiment": "https://santiment.net",
        "Binance Blog": "https://www.binance.com/en/blog"
    }
    result = []
    try:
        async with aiohttp.ClientSession() as session:
            for name, url in other_sites.items():
                try:
                    async with session.get(url, timeout=10) as response:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        links = soup.find_all("a", href=True)
                        for tag in links:
                            href = tag["href"]
                            if href.startswith("http") and name.lower() in href.lower():
                                title = tag.get_text(strip=True)[:100]
                                result.append((f"[{name}] {title}", href))
                                break
                except:
                    continue
        return result
    except Exception as e:
        print(f"Error fetching other sites news: {e}")
        return []

async def fetch_telegram_channel_news(channel_username="WatcherGuru"):
    url = f"https://t.me/s/{channel_username}"
    try:
        browser = await launch(headless=True, args=['--no-sandbox'])
        page = await browser.newPage()
        await page.goto(url, timeout=60000)
        content = await page.content()
        await browser.close()

        soup = BeautifulSoup(content, 'html.parser')
        posts = soup.select('.tgme_widget_message_text')

        news_items = []
        for post in posts[:10]:
            text = post.get_text(strip=True)
            news_items.append((text[:100], url))
        return news_items
    except Exception as e:
        print(f"Error fetching telegram channel news: {e}")
        return []