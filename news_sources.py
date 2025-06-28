import requests
from bs4 import BeautifulSoup

def fetch_watcher_guru_news():
    url = "https://watcher.guru"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("a.home-news-card")
    news_items = []
    for a in articles[:10]:
        title = a.get("title") or a.get_text(strip=True)
        href = a.get("href")
        full_url = f"https://watcher.guru{href}" if href else ""
        if title and full_url:
            news_items.append((title, full_url))
    return news_items

def fetch_other_sites_news():
    # Placeholder logic - replace with actual scraping logic
    return []