import requests
from bs4 import BeautifulSoup
from .base import BaseParser, Announcement

class BinanceParser(BaseParser):
    URL = "https://www.binance.com/en/support/announcement"

    def fetch(self):
        r = requests.get(self.URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []

        for a in soup.select("a.css-1ej4hfo"):
            title = a.text.lower()
            url = "https://www.binance.com" + a["href"]

            if "list" in title or "delist" in title:
                category = "listing" if "list" in title else "delisting"
                market = "futures" if "futures" in title else "spot"

                results.append(
                    Announcement("Binance", a.text, url, category, market)
                )

        return results
