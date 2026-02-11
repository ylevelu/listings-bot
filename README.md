# 📈 Crypto Listings & Announcements Bot

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A powerful Telegram bot that monitors **real-time listings, delistings, and official announcements** from top cryptocurrency exchanges.  
Get instant notifications about new trading pairs and upcoming listings directly in your Telegram channel.

---

## ✨ Features

✅ **Live Spot Listings** – detects new pairs as soon as they appear in exchange APIs.  
✅ **Spot Delistings** – alerts when a trading pair is removed.  
✅ **Announcement Scanner** – parses official RSS/HTML news for **pre‑listing announcements** (Binance, Bybit, MEXC, Gate.io, KuCoin, Bitget).  
✅ **Smart First Run** – no spam; saves current state without sending anything.  
✅ **Persistent State** – stores known pairs in JSON files to track only real changes.  
✅ **Fully Customizable** – easy to add more exchanges or adjust check intervals.  
✅ **Clean English Logs** – no encoding issues on Windows.  
✅ **24/7 Operation** – designed to run continuously on a VPS or local machine.

---

## 🔧 Supported Exchanges

| Exchange   | Spot Listings | Spot Delistings | Announcements |
|------------|---------------|-----------------|---------------|
| Binance    | ✅            | ✅              | ✅ (RSS)      |
| KuCoin     | ✅            | ✅              | ✅ (HTML)     |
| Gate.io    | ✅            | ✅              | ✅ (HTML)     |
| MEXC       | ✅            | ✅              | ✅ (HTML)     |
| LBank      | ✅            | ✅              | ❌            |
| Upbit      | ✅            | ✅              | ❌            |
| Bybit      | ✅            | ✅              | ✅ (HTML)     |
| OKX        | ✅            | ✅              | ❌            |
| Bitget     | ✅            | ✅              | ✅ (HTML)     |
| BingX      | ✅            | ✅              | ❌            |

*More exchanges can be added easily – contributions welcome!*

---

## 🧠 How It Works

1. **First launch** – bot fetches all trading pairs from each exchange and saves them into `data/` folder. No Telegram messages are sent.
2. **Subsequent launches** – bot fetches current pairs again, compares with saved state:
   - **New pairs** → sends `Binance BTCUSDT Live on Spot`
   - **Missing pairs** → sends `Binance to Delist XRP from Spot`
3. **Announcement module** – periodically checks official news sources, extracts upcoming listing information, and sends messages like `Binance to List AZTEC on Spot (https://...)`
4. All messages are sent to your Telegram channel **without extra clutter** – just the facts.

---

## 📋 Prerequisites

- Python **3.8 or higher**
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- A Telegram channel/group where the bot is an **administrator**
- Git (optional, for cloning)

---

## 🚀 Installation & Configuration

### 1. Clone the repository
```bash
git clone https://github.com/ylevelu/listings-bot.git
cd listings-bot
2. Install dependencies

pip install -r requirements.txt
If you don't have requirements.txt, create it:


pip install requests python-telegram-bot feedparser beautifulsoup4 lxml
3. Set up your credentials
Create config_pkg/setting.py (this file is ignored by Git):


TELEGRAM_TOKEN = "1234567890:ABCdef..."   # your bot token
TELEGRAM_CHANNEL_ID = "@your_channel"     # or numeric ID like -1001234567890
4. (Optional) Test Telegram connection
Create a file test_send.py:


from notifier.telegram import send
send("✅ Bot is ready!")
Run it:


python test_send.py
Check your channel – you should see the message.

▶️ Usage
Start the bot

python main.py
The bot will immediately begin its first check cycle – no Telegram messages will be sent yet, only local state files are created.

After the first cycle, the bot sleeps for 300 seconds (5 minutes) and then starts again. From now on, every change will be reported.

To keep the bot running 24/7:

Windows: run pythonw main.py (no console window) or use Task Scheduler.

Linux/macOS: use nohup or screen / tmux.

Example with nohup:

nohup python3 main.py > bot.log 2>&1 &
📁 Project Structure

crypto-listings-bot/
│
├─ config_pkg/           # configuration package
│   ├─ __init__.py
│   └─ setting.py        # your private token/channel (IGNORED by git)
│
├─ notifier/             # Telegram sending module
│   ├─ __init__.py
│   └─ telegram.py
│
├─ parsers/              # exchange parsers
│   ├─ __init__.py
│   ├─ base.py          # abstract base class
│   ├─ binance.py
│   ├─ kucoin.py
│   ├─ gate.py
│   ├─ mexc.py
│   ├─ lbank.py
│   ├─ upbit.py
│   ├─ bybit.py
│   ├─ okx.py
│   ├─ bitget.py
│   ├─ bingx.py
│   └─ announcements.py # all announcement parsers
│
├─ data/                 # created automatically, stores state JSONs
├─ logs/                 # created automatically, bot logs
├─ .gitignore           # ignores secrets, data, logs, cache
├─ main.py              # main bot loop
├─ requirements.txt     # dependencies
└─ README.md            # this file

```

## 📰 Announcements Parsing – How to Add More Exchanges
#### The file parsers/announcements.py contains classes for each exchange that provides official listing news.
#### To add a new source:

##### Create a new class (e.g. KucoinAnnouncementParser).

##### Implement get_new_announcements(self):

##### Fetch the webpage / RSS feed.

##### Parse relevant articles.

##### Compare with previously sent IDs (store in data/).

##### Return a list of announcement dictionaries.

##### Include the parser in get_all_announcements().

##### Example pattern – see existing parsers (Binance, Bybit, etc.) for reference.

## 📬 Contact
#### Maintainer: Serhii
#### GitHub: @ylevelu
#### Telegram: https://t.me/aslgw / https://t.me/LBScalp
#### Mail: serhiimikhalkov@icloud.com / sergejmihalkov@gmail.com
#### Project link: https://github.com/ylevelu/listings-bot
