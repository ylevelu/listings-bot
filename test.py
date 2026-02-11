# test_telegram.py
from notifier.telegram import send
from parsers.base import Announcement

ann = Announcement(
    exchange="TEST_EXCHANGE",
    title="TEST listing futures BTC/USDT",
    url="https://example.com",
    category="listing",
    market_type="futures"
)

send(ann)
print("Тестовое сообщение отправлено в Telegram")
