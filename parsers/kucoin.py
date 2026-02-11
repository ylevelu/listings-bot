import requests
from .base import BaseParser, Announcement

class KucoinParser(BaseParser):
    API = "https://www.kucoin.com/_api/cms/articles"

    def fetch(self):
        r = requests.get(self.API, params={"page":1,"pageSize":20})
        data = r.json()["items"]
        results = []

        for item in data:
            title = item["title"].lower()
            if "list" in title or "delist" in title:
                category = "listing" if "list" in title else "delisting"
                market = "futures" if "futures" in title else "spot"
                url = f"https://www.kucoin.com/news/{item['id']}"

                results.append(
                    Announcement("KuCoin", item["title"], url, category, market)
                )
        return results
