import requests
from bs4 import BeautifulSoup
from .base import BaseParser, Announcement

class MexcParser(BaseParser):
    URL = "https://www.mexc.com/ru-RU/announcements/all"

    def fetch(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        try:
            r = requests.get(self.URL, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            print("MEXC request failed:", e)
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        results = []

        # На текущей странице анонсы лежат в <div class="news-item"> с <a> внутри
        for a in soup.select("div.news-item a"):
            title = a.get_text(strip=True)
            href = a.get("href", "")
            if not title or not href:
                continue
            url = "https://www.mexc.com" + href

            title_l = title.lower()
            # Определяем листинг / делистинг
            if "list" in title_l or "delist" in title_l:
                category = "listing" if "list" in title_l else "delisting"
                # Определяем futures / spot
                market = "futures" if any(x in title_l for x in ["future", "perpetual"]) else "spot"

                results.append(
                    Announcement("MEXC", title, url, category, market)
                )

        return results
