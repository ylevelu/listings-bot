# parsers/upbit.py
from .base import BaseParser

class UpbitParser(BaseParser):
    EXCHANGE_NAME = "Upbit"
    API_URL = "https://api.upbit.com/v1/market/all"

    def _parse_response(self, data):
        symbols = []
        for item in data:
            market = item['market']
            if market.startswith('KRW-') or market.startswith('BTC-'):
                symbols.append(market.split('-')[1])
        return symbols