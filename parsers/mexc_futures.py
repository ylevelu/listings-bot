import requests
import json
import os
from models import Announcement

STORAGE_FILE = "storage/contracts.json"


class MexcFuturesDetector:
    def __init__(self):
        self.api_url = "https://contract.mexc.com/api/v1/contract/detail"
        self.exchange = "MEXC"

    def load_storage(self):
        if not os.path.exists(STORAGE_FILE):
            return {}

        with open(STORAGE_FILE, "r") as f:
            return json.load(f)

    def save_storage(self, data):
        os.makedirs("storage", exist_ok=True)
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def fetch_contracts(self):
        try:
            r = requests.get(self.api_url, timeout=15)
            r.raise_for_status()
            data = r.json()
            return [c["symbol"] for c in data.get("data", [])]
        except Exception as e:
            print(f"MEXC Futures API error: {e}")
            return []

    def detect(self):
        storage = self.load_storage()

        old_contracts = set(storage.get("mexc_futures", []))
        current_contracts = set(self.fetch_contracts())

        new_contracts = current_contracts - old_contracts

        storage["mexc_futures"] = list(current_contracts)
        self.save_storage(storage)

        announcements = []

        for symbol in new_contracts:
            url_symbol = symbol.replace("_", "")
            url = f"https://www.mexc.com/futures/{symbol}"

            announcements.append(
                Announcement(
                    exchange=self.exchange,
                    category="listing",
                    market="futures",
                    title=f"{symbol} Live on MEXC Futures",
                    url=url
                )
            )

        return announcements
