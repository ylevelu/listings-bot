import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sent (
    exchange TEXT,
    title TEXT
)
""")
conn.commit()


def is_sent(exchange, title):
    cur.execute(
        "SELECT 1 FROM sent WHERE exchange=? AND title=?",
        (exchange, title)
    )
    return cur.fetchone() is not None


def mark_sent(exchange, title):
    cur.execute(
        "INSERT INTO sent VALUES (?, ?)",
        (exchange, title)
    )
    conn.commit()
