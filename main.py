import sys
from pathlib import Path
import json
import time
import logging
from datetime import datetime

ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from notifier.telegram import send
from parsers.binance import BinanceParser
from parsers.kucoin import KucoinParser
from parsers.gate import GateParser
from parsers.mexc import MexcParser
from parsers.lbank import LBankParser
from parsers.upbit import UpbitParser
from parsers.bybit import BybitParser
from parsers.okx import OKXParser
from parsers.bitget import BitgetParser
from parsers.bingx import BingxParser
from parsers.announcements import get_all_announcements

# ============ CONFIG ============
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

CHECK_INTERVAL = 75  # 1 minut 15 seconds, to avoid hitting rate limits

# ============ SPOT PARSERS ============
SPOT_PARSERS = [
    BinanceParser(),
    KucoinParser(),
    GateParser(),
    MexcParser(),
    LBankParser(),
    UpbitParser(),
    BybitParser(),
    OKXParser(),
    BitgetParser(),
    BingxParser()
]

# ============ STATE MANAGEMENT ============
def load_previous_state(exchange_name):
    file_path = DATA_DIR / f"{exchange_name.lower()}.json"
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return None

def save_current_state(exchange_name, symbols):
    file_path = DATA_DIR / f"{exchange_name.lower()}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(list(symbols), f, indent=2)

# ============ MESSAGE FORMATTING ============
def format_new_pair(exchange, symbol, market="Spot", link=None):
    base = f"{exchange} {symbol} Live on {market}"
    if link:
        return f"{base} ({link})"
    return base

def format_delisting(exchange, symbol, market="Spot"):
    return f"{exchange} to Delist {symbol} from {market}"

def format_announcement(ann):
    if ann["type"] == "announcement_listing_spot":
        return f"{ann['exchange']} to List {ann['symbol']} on {ann['market']} ({ann['link']})"
    elif ann["type"] == "announcement_listing_futures":
        return f"{ann['exchange']} to List {ann['symbol']} on {ann['market']} ({ann['link']})"
    return None

# ============ EXCHANGE CHECKER ============
def check_exchange(parser):
    exchange_name = parser.EXCHANGE_NAME
    logger.info(f"Processing {exchange_name}...")
    
    try:
        current_symbols = set(parser.fetch_listings())
    except Exception as e:
        logger.error(f"{exchange_name} fetch error: {e}")
        return []
    
    if not current_symbols:
        logger.warning(f"{exchange_name} no data")
        return []
    
    previous = load_previous_state(exchange_name)
    is_first_run = previous is None
    
    if is_first_run:
        save_current_state(exchange_name, current_symbols)
        logger.info(f"{exchange_name} first run, saved {len(current_symbols)} pairs")
        return []
    
    new_pairs = current_symbols - previous
    delisted_pairs = previous - current_symbols
    
    save_current_state(exchange_name, current_symbols)
    
    messages = []
    
    for symbol in sorted(new_pairs)[:20]:
        messages.append(format_new_pair(exchange_name, symbol, "Spot"))
    
    for symbol in sorted(delisted_pairs)[:10]:
        messages.append(format_delisting(exchange_name, symbol, "Spot"))
    
    if new_pairs:
        logger.info(f"{exchange_name} new: {len(new_pairs)}")
    if delisted_pairs:
        logger.info(f"{exchange_name} delisted: {len(delisted_pairs)}")
    
    return messages

# ============ ANNOUNCEMENT CHECKER ============
def check_announcements():
    logger.info("Checking announcements...")
    messages = []
    
    announcements = get_all_announcements()
    for ann in announcements:
        msg = format_announcement(ann)
        if msg:
            messages.append(msg)
            logger.info(f"Announcement: {ann['exchange']} {ann['symbol']} {ann['market']}")
    
    return messages

# ============ MAIN CYCLE ============
def run_once():
    logger.info("=" * 50)
    logger.info("Starting check cycle")
    
    all_messages = []
    
    # 1. Check spot exchanges
    for parser in SPOT_PARSERS:
        msgs = check_exchange(parser)
        all_messages.extend(msgs)
        time.sleep(1)
    
    # 2. Check announcements
    announcement_msgs = check_announcements()
    all_messages.extend(announcement_msgs)
    
    # 3. Send all messages
    for i, msg in enumerate(all_messages[:50], 1):
        try:
            success = send(msg)
            if success:
                logger.info(f"Sent [{i}/50]: {msg[:50]}...")
            else:
                logger.error(f"Failed to send [{i}/50]: {msg[:50]}...")
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Send error [{i}/50]: {e}")
    
    if not all_messages:
        logger.info("No changes or announcements")
    
    logger.info("Check cycle finished")

# ============ START ============
def main():
    logger.info("=== Listings & Announcements Bot Started ===")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
    
    while True:
        try:
            run_once()
        except Exception as e:
            logger.exception("Critical error, continuing...")
        finally:
            logger.info(f"Next check in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()