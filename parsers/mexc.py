# parsers/mexc.py
from .base import BaseParser

class MexcParser(BaseParser):
    EXCHANGE_NAME = "MEXC"
    API_URL = "https://api.mexc.com/api/v3/exchangeInfo"

    def _parse_response(self, data):
        symbols = []
        for s in data.get('symbols', []):
            if s['status'] == '1':
                symbols.append(s['symbol'])
        return symbols