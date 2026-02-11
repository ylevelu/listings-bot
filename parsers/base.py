# parsers/base.py
import requests

class BaseParser:
    EXCHANGE_NAME = "Base"
    API_URL = ""

    def fetch_listings(self):
        try:
            response = requests.get(self.API_URL, timeout=15)
            response.raise_for_status()
            return self._parse_response(response.json())
        except Exception as e:
            print(f"! {self.EXCHANGE_NAME} error: {e}")
            return []

    def _parse_response(self, data):
        raise NotImplementedError