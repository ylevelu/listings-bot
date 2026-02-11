# parsers/okx.py
from .base import BaseParser

class OKXParser(BaseParser):
    EXCHANGE_NAME = "OKX"
    API_URL = "https://www.okx.com/api/v5/public/instruments?instType=SPOT"

    def _parse_response(self, data):
        symbols = []
        for item in data.get('data', []):
            if item['state'] == 'live':
                symbols.append(item['instId'].replace('-', ''))
        return symbols