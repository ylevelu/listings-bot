# parsers/gate.py
from .base import BaseParser

class GateParser(BaseParser):
    EXCHANGE_NAME = "Gate.io"
    API_URL = "https://api.gateio.ws/api/v4/spot/currency_pairs"

    def _parse_response(self, data):
        symbols = []
        for pair in data:
            if pair.get('trade_status') == 'tradable':
                symbols.append(pair['id'].replace('_', ''))
        return symbols