# parsers/bingx.py
from .base import BaseParser
import requests

class BingxParser(BaseParser):
    EXCHANGE_NAME = "BingX"
    API_URL = "https://open-api.bingx.com/openApi/spot/v1/common/symbols"

    def fetch_listings(self):
        try:
            response = requests.get(self.API_URL, timeout=15)
            data = response.json()
            if data.get('code') == 0:
                return self._parse_response(data)
            return []
        except Exception as e:
            print(f"! BingX error: {e}")
            return []

    def _parse_response(self, data):
        symbols = []
        for s in data.get('data', []):
            if s.get('state') == 1:  # 1 = trading
                symbols.append(s['symbol'])
        return symbols