import requests
from bs4 import BeautifulSoup
from .base import BaseParser, Announcement


class GateParser(BaseParser):
    URL = "https://www.gate.io/announcements"

    def fetch(self):
        r = requests.get(self.URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []

        for a in soup.select("a.announcement-item"):
            title = a.text.strip()
            title_l = title.lower()
            url = "https://www.gate.io" + a["href"]

            if "list" in title_l or "delist" in title_l:
                category = "listing" if "list" in title_l else "delisting"
                market = "futures" if any(x in title_l for x in ["futures", "perpetual"]) else "spot"

                results.append(
                    Announcement("Gate", title, url, category, market)
                )

        return results
