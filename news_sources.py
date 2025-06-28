import aiohttp
from bs4 import BeautifulSoup

async def fetch_watcher_guru_news():
    url = "https://watcher.guru"
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

async def fetch_other_sites_news():
    result = []
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
            except Exception:
                pass
    return result
