import requests
from bs4 import BeautifulSoup
from .base import BaseParser, Announcement


class UpbitParser(BaseParser):
    URL = "https://upbit.com/service_center/notice"

    def fetch(self):
        r = requests.get(self.URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []

        for a in soup.select("a.link"):
            title = a.text.strip()
            title_l = title.lower()
            url = "https://upbit.com" + a["href"]

            if "list" in title_l or "delist" in title_l:
                category = "listing" if "list" in title_l else "delisting"
                market = "spot"  # Upbit = только spot

                results.append(
                    Announcement("Upbit", title, url, category, market)
                )

        return results
