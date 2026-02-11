# parsers/announcements.py
import feedparser
import requests
import re
import json
import time
from pathlib import Path
from bs4 import BeautifulSoup

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ============ BINANCE (RSS) ============
class BinanceAnnouncementParser:
    EXCHANGE_NAME = "Binance"
    RSS_URL = "https://www.binance.com/en/rss/announcements"
    STATE_FILE = DATA_DIR / "binance_announcements.json"

    def get_new_announcements(self):
        try:
            feed = feedparser.parse(self.RSS_URL)
            current_ids = {entry.link for entry in feed.entries[:30]}
            
            if self.STATE_FILE.exists():
                with open(self.STATE_FILE, 'r', encoding='utf-8') as f:
                    old_ids = set(json.load(f))
            else:
                old_ids = set()
            
            new_ids = current_ids - old_ids
            with open(self.STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(current_ids), f)
            
            results = []
            for entry in feed.entries:
                if entry.link in new_ids:
                    title = entry.title
                    
                    # Spot Listings
                    spot_match = re.search(r"Will List\s+([A-Za-z0-9]+)(?:\s*\(?([A-Z]+)\)?)?", title, re.IGNORECASE)
                    if spot_match:
                        symbol = spot_match.group(2) or spot_match.group(1)
                        results.append({
                            "type": "announcement_listing_spot",
                            "exchange": self.EXCHANGE_NAME,
                            "symbol": symbol.upper(),
                            "market": "Spot",
                            "link": entry.link,
                            "title": title
                        })
                        continue
                    
                    # Futures Listings
                    futures_match = re.search(r"Will List\s+([A-Za-z0-9]+).*?(Futures|USDⓈ-M)", title, re.IGNORECASE)
                    if futures_match:
                        symbol = futures_match.group(1)
                        results.append({
                            "type": "announcement_listing_futures",
                            "exchange": self.EXCHANGE_NAME,
                            "symbol": symbol.upper(),
                            "market": "Futures",
                            "link": entry.link,
                            "title": title
                        })
            return results
        except Exception as e:
            print(f"! Binance Announcements error: {e}")
            return []

# ============ BYBIT (HTML) ============
class BybitAnnouncementParser:
    EXCHANGE_NAME = "Bybit"
    URL = "https://announcements.bybit.com/en-US/"
    STATE_FILE = DATA_DIR / "bybit_announcements.json"

    def get_new_announcements(self):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(self.URL, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            current_links = []
            for article in soup.select('article a')[:20]:
                href = article.get('href', '')
                if href.startswith('/'):
                    link = "https://announcements.bybit.com" + href
                else:
                    link = href
                current_links.append(link)
            current_ids = set(current_links)
            
            if self.STATE_FILE.exists():
                with open(self.STATE_FILE, 'r', encoding='utf-8') as f:
                    old_ids = set(json.load(f))
            else:
                old_ids = set()
            
            new_ids = current_ids - old_ids
            with open(self.STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(current_ids), f)
            
            results = []
            for article in soup.select('article'):
                link_elem = article.select_one('a')
                if not link_elem:
                    continue
                
                href = link_elem.get('href', '')
                if href.startswith('/'):
                    link = "https://announcements.bybit.com" + href
                else:
                    link = href
                
                if link not in new_ids:
                    continue
                
                title = link_elem.text.strip()
                
                spot_match = re.search(r"to List\s+([A-Za-z0-9]+).*?on Spot", title, re.IGNORECASE)
                if spot_match:
                    results.append({
                        "type": "announcement_listing_spot",
                        "exchange": self.EXCHANGE_NAME,
                        "symbol": spot_match.group(1).upper(),
                        "market": "Spot",
                        "link": link,
                        "title": title
                    })
                
                futures_match = re.search(r"to List\s+([A-Za-z0-9]+).*?Futures", title, re.IGNORECASE)
                if futures_match:
                    results.append({
                        "type": "announcement_listing_futures",
                        "exchange": self.EXCHANGE_NAME,
                        "symbol": futures_match.group(1).upper(),
                        "market": "Futures",
                        "link": link,
                        "title": title
                    })
            return results
        except Exception as e:
            print(f"! Bybit Announcements error: {e}")
            return []

# ============ MEXC (HTML) ============
class MexcAnnouncementParser:
    EXCHANGE_NAME = "MEXC"
    URL = "https://www.mexc.com/news/listing"
    STATE_FILE = DATA_DIR / "mexc_announcements.json"

    def get_new_announcements(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            response = requests.get(self.URL, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            current_links = []
            announcements = []
            
            # MEXC announcements structure
            for item in soup.select('a.news-item, .listing-item a, .announcement-item a')[:20]:
                href = item.get('href', '')
                if href:
                    if href.startswith('/'):
                        link = "https://www.mexc.com" + href
                    elif href.startswith('http'):
                        link = href
                    else:
                        link = "https://www.mexc.com/" + href
                    current_links.append(link)
                    
                    title = item.text.strip() or item.get('title', '')
                    if not title:
                        parent = item.find_parent('div', class_=re.compile('item|news|listing'))
                        if parent:
                            title = parent.text.strip()
                    
                    announcements.append({
                        'link': link,
                        'title': title
                    })
            
            current_ids = set(current_links)
            
            if self.STATE_FILE.exists():
                with open(self.STATE_FILE, 'r', encoding='utf-8') as f:
                    old_ids = set(json.load(f))
            else:
                old_ids = set()
            
            new_ids = current_ids - old_ids
            with open(self.STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(current_ids), f)
            
            results = []
            for ann in announcements:
                if ann['link'] in new_ids:
                    title = ann['title']
                    
                    # Ищем листинги
                    listing_match = re.search(r"Lists?\s+([A-Za-z0-9]+)(?:\s*\(?([A-Z]+)\)?)?", title, re.IGNORECASE)
                    if listing_match:
                        symbol = listing_match.group(2) or listing_match.group(1)
                        results.append({
                            "type": "announcement_listing_spot",
                            "exchange": self.EXCHANGE_NAME,
                            "symbol": symbol.upper(),
                            "market": "Spot",
                            "link": ann['link'],
                            "title": title
                        })
                    
                    # Ищем фьючерсы
                    futures_match = re.search(r"Futures.*?([A-Za-z0-9]+)", title, re.IGNORECASE)
                    if futures_match and not listing_match:
                        symbol = futures_match.group(1)
                        results.append({
                            "type": "announcement_listing_futures",
                            "exchange": self.EXCHANGE_NAME,
                            "symbol": symbol.upper(),
                            "market": "Futures",
                            "link": ann['link'],
                            "title": title
                        })
            return results
        except Exception as e:
            print(f"! MEXC Announcements error: {e}")
            return []

# ============ GATE.IO (HTML) ============
class GateAnnouncementParser:
    EXCHANGE_NAME = "Gate.io"
    URL = "https://www.gate.io/announcements"
    STATE_FILE = DATA_DIR / "gate_announcements.json"

    def get_new_announcements(self):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(self.URL, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            current_links = []
            announcements = []
            
            for link in soup.select('a.announcement__link, .article-item a, .news-item a')[:20]:
                href = link.get('href', '')
                if href:
                    if href.startswith('/'):
                        full_link = "https://www.gate.io" + href
                    else:
                        full_link = href
                    current_links.append(full_link)
                    announcements.append({
                        'link': full_link,
                        'title': link.text.strip() or link.get('title', '')
                    })
            
            current_ids = set(current_links)
            
            if self.STATE_FILE.exists():
                with open(self.STATE_FILE, 'r', encoding='utf-8') as f:
                    old_ids = set(json.load(f))
            else:
                old_ids = set()
            
            new_ids = current_ids - old_ids
            with open(self.STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(current_ids), f)
            
            results = []
            for ann in announcements:
                if ann['link'] in new_ids:
                    title = ann['title']
                    
                    listing_match = re.search(r"Lists?\s+([A-Za-z0-9]+)", title, re.IGNORECASE)
                    if listing_match:
                        results.append({
                            "type": "announcement_listing_spot",
                            "exchange": self.EXCHANGE_NAME,
                            "symbol": listing_match.group(1).upper(),
                            "market": "Spot",
                            "link": ann['link'],
                            "title": title
                        })
            return results
        except Exception as e:
            print(f"! Gate.io Announcements error: {e}")
            return []

# ============ KUCOIN (HTML) ============
class KucoinAnnouncementParser:
    EXCHANGE_NAME = "KuCoin"
    URL = "https://www.kucoin.com/ru/news/categories/listings"
    STATE_FILE = DATA_DIR / "kucoin_announcements.json"

    def get_new_announcements(self):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(self.URL, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            current_links = []
            announcements = []
            
            for link in soup.select('a.news-item, .article-link, .post-link')[:20]:
                href = link.get('href', '')
                if href:
                    if href.startswith('/'):
                        full_link = "https://www.kucoin.com" + href
                    else:
                        full_link = href
                    current_links.append(full_link)
                    announcements.append({
                        'link': full_link,
                        'title': link.text.strip() or link.get('title', '')
                    })
            
            current_ids = set(current_links)
            
            if self.STATE_FILE.exists():
                with open(self.STATE_FILE, 'r', encoding='utf-8') as f:
                    old_ids = set(json.load(f))
            else:
                old_ids = set()
            
            new_ids = current_ids - old_ids
            with open(self.STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(current_ids), f)
            
            results = []
            for ann in announcements:
                if ann['link'] in new_ids:
                    title = ann['title']
                    
                    listing_match = re.search(r"Listing of\s+([A-Za-z0-9]+)", title, re.IGNORECASE)
                    if listing_match:
                        results.append({
                            "type": "announcement_listing_spot",
                            "exchange": self.EXCHANGE_NAME,
                            "symbol": listing_match.group(1).upper(),
                            "market": "Spot",
                            "link": ann['link'],
                            "title": title
                        })
            return results
        except Exception as e:
            print(f"! KuCoin Announcements error: {e}")
            return []

# ============ BITGET (HTML) ============
class BitgetAnnouncementParser:
    EXCHANGE_NAME = "Bitget"
    URL = "https://www.bitget.com/news/category/listing-announcement"
    STATE_FILE = DATA_DIR / "bitget_announcements.json"

    def get_new_announcements(self):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(self.URL, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            current_links = []
            announcements = []
            
            for link in soup.select('a.news-item, .article-item, .announcement-item a')[:20]:
                href = link.get('href', '')
                if href:
                    if href.startswith('/'):
                        full_link = "https://www.bitget.com" + href
                    else:
                        full_link = href
                    current_links.append(full_link)
                    announcements.append({
                        'link': full_link,
                        'title': link.text.strip() or link.get('title', '')
                    })
            
            current_ids = set(current_links)
            
            if self.STATE_FILE.exists():
                with open(self.STATE_FILE, 'r', encoding='utf-8') as f:
                    old_ids = set(json.load(f))
            else:
                old_ids = set()
            
            new_ids = current_ids - old_ids
            with open(self.STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(current_ids), f)
            
            results = []
            for ann in announcements:
                if ann['link'] in new_ids:
                    title = ann['title']
                    
                    listing_match = re.search(r"to List\s+([A-Za-z0-9]+)", title, re.IGNORECASE)
                    if listing_match:
                        results.append({
                            "type": "announcement_listing_spot",
                            "exchange": self.EXCHANGE_NAME,
                            "symbol": listing_match.group(1).upper(),
                            "market": "Spot",
                            "link": ann['link'],
                            "title": title
                        })
            return results
        except Exception as e:
            print(f"! Bitget Announcements error: {e}")
            return []

# ============ ГЛАВНАЯ ФУНКЦИЯ ============
# ============ MAIN FUNCTION ============
def get_all_announcements():
    """Collect announcements from all exchanges"""
    results = []
    
    print("! Collecting announcements from all exchanges...")
    
    # Binance
    try:
        binance = BinanceAnnouncementParser()
        binance_anns = binance.get_new_announcements()
        print(f"  Binance: {len(binance_anns)}")
        results.extend(binance_anns)
    except Exception as e:
        print(f"  Binance error: {e}")
    
    # Bybit
    try:
        bybit = BybitAnnouncementParser()
        bybit_anns = bybit.get_new_announcements()
        print(f"  Bybit: {len(bybit_anns)}")
        results.extend(bybit_anns)
    except Exception as e:
        print(f"  Bybit error: {e}")
    
    # MEXC
    try:
        mexc = MexcAnnouncementParser()
        mexc_anns = mexc.get_new_announcements()
        print(f"  MEXC: {len(mexc_anns)}")
        results.extend(mexc_anns)
    except Exception as e:
        print(f"  MEXC error: {e}")
    
    # Gate.io
    try:
        gate = GateAnnouncementParser()
        gate_anns = gate.get_new_announcements()
        print(f"  Gate.io: {len(gate_anns)}")
        results.extend(gate_anns)
    except Exception as e:
        print(f"  Gate.io error: {e}")
    
    # KuCoin
    try:
        kucoin = KucoinAnnouncementParser()
        kucoin_anns = kucoin.get_new_announcements()
        print(f"  KuCoin: {len(kucoin_anns)}")
        results.extend(kucoin_anns)
    except Exception as e:
        print(f"  KuCoin error: {e}")
    
    # Bitget
    try:
        bitget = BitgetAnnouncementParser()
        bitget_anns = bitget.get_new_announcements()
        print(f"  Bitget: {len(bitget_anns)}")
        results.extend(bitget_anns)
    except Exception as e:
        print(f"  Bitget error: {e}")
    
    print(f"! Total announcements found: {len(results)}")
    return results