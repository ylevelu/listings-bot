import time
import traceback

from parsers.binance import BinanceParser
from parsers.kucoin import KucoinParser
from parsers.gate import GateParser
from parsers.mexc import MexcParser
from parsers.lbank import LBankParser
from parsers.upbit import UpbitParser

from storage.sqlite import is_sent, mark_sent
from notifier.telegram import send
from config.settings import CHECK_INTERVAL_SECONDS


PARSERS = [
    BinanceParser(),
    KucoinParser(),
    GateParser(),
    MexcParser(),
    LBankParser(),
    UpbitParser(),
]


def run():
    print("Crypto Listings Bot started")

    while True:
        for parser in PARSERS:
            parser_name = parser.__class__.__name__
            try:
                announcements = parser.fetch()
                for ann in announcements:
                    if not is_sent(ann.exchange, ann.title):
                        send(ann)
                        mark_sent(ann.exchange, ann.title)
                        print(f"Sent: {ann.exchange} | {ann.title}")
            except Exception as e:
                print(f"Error in {parser_name}: {e}")
                traceback.print_exc()

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
