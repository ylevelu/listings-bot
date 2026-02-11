import requests
from bs4 import BeautifulSoup
from .base import BaseParser, Announcement


class LBankParser(BaseParser):
    URL = "https://www.lbank.com/support"

    def fetch(self):
        r = requests.get(self.URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []

        for a in soup.select("a.article-item"):
            title = a.text.strip()
            title_l = title.lower()
            url = "https://www.lbank.com" + a["href"]

            if "list" in title_l or "delist" in title_l:
                category = "listing" if "list" in title_l else "delisting"
                market = "futures" if "contract" in title_l else "spot"

                results.append(
                    Announcement("LBank", title, url, category, market)
                )

        return results
