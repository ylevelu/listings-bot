import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from notifier.telegram import send

result = send("Bot test message")
print(f"Send result: {result}")