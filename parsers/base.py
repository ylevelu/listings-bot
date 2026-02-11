from abc import ABC, abstractmethod

class Announcement:
    def __init__(self, exchange, title, url, category, market_type):
        self.exchange = exchange       # название биржи
        self.title = title             # заголовок анонса
        self.url = url                 # ссылка на статью
        self.category = category       # listing / delisting
        self.market_type = market_type # spot / futures

class BaseParser(ABC):
    @abstractmethod
    def fetch(self) -> list[Announcement]:
        pass
