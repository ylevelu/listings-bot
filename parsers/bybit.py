# parsers/bybit.py
from .base import BaseParser

class BybitParser(BaseParser):
    EXCHANGE_NAME = "Bybit"
    API_URL = "https://api.bybit.com/v5/market/instruments-info?category=spot"

    def _parse_response(self, data):
        symbols = []
        for item in data.get('result', {}).get('list', []):
            if item['status'] == 'Trading':
                symbols.append(item['symbol'])
        return symbols