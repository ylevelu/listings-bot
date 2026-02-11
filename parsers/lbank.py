# parsers/lbank.py
from .base import BaseParser

class LBankParser(BaseParser):
    EXCHANGE_NAME = "LBank"
    API_URL = "https://api.lbkex.com/v2/currencyPairs.do?symbol=all"

    def _parse_response(self, data):
        pairs = data.get('result', [])
        return [p.replace('_', '').upper() for p in pairs]