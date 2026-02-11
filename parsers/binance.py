# parsers/binance.py
from .base import BaseParser

class BinanceParser(BaseParser):
    EXCHANGE_NAME = "Binance"
    API_URL = "https://api.binance.com/api/v3/exchangeInfo"

    def _parse_response(self, data):
        symbols = []
        for s in data.get('symbols', []):
            if s['status'] == 'TRADING':
                symbols.append(s['symbol'])
        return symbols