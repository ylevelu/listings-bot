# parsers/bitget.py
from .base import BaseParser
import requests

class BitgetParser(BaseParser):
    EXCHANGE_NAME = "Bitget"
    API_URL = "https://api.bitget.com/api/v2/spot/public/symbols"

    def fetch_listings(self):
        try:
            response = requests.get(self.API_URL, timeout=15)
            data = response.json()
            if data.get('code') == '00000':
                return self._parse_response(data)
            return []
        except Exception as e:
            print(f"! Bitget error: {e}")
            return []

    def _parse_response(self, data):
        symbols = []
        for s in data.get('data', []):
            if s.get('status') == 'online':
                symbols.append(s['symbolName'])
        return symbols