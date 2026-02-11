# test_announcements.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from parsers.announcements import get_all_announcements

print("=" * 60)
print("ANNOUNCEMENT PARSER TEST - ALL EXCHANGES")
print("=" * 60)

# Get announcements from all exchanges
announcements = get_all_announcements()

print("\n" + "=" * 60)
print(f"TOTAL ANNOUNCEMENTS FOUND: {len(announcements)}")
print("=" * 60)

# Show details
if announcements:
    for i, ann in enumerate(announcements, 1):
        print(f"\n{i}. {ann['exchange']} - {ann['symbol']}")
        print(f"   Type: {ann['type']}")
        print(f"   Market: {ann['market']}")
        print(f"   Link: {ann['link']}")
        print(f"   Title: {ann['title'][:100]}...")
else:
    print("\n! No announcements found. This is normal if no exchanges have announced new listings.")

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)