# parsers/kucoin.py
from .base import BaseParser

class KucoinParser(BaseParser):
    EXCHANGE_NAME = "KuCoin"
    API_URL = "https://api.kucoin.com/api/v1/symbols"

    def _parse_response(self, data):
        symbols = []
        for s in data.get('data', []):
            if s.get('enableTrading', False):
                symbols.append(s['symbol'])
        return symbols