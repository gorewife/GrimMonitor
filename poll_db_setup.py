# poll_db_setup.py
# Run this script once to create the poll_stats.db SQLite database and schema in GrimMonitor
import sqlite3
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'poll_stats.db'))

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS poll_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    total_votes INTEGER NOT NULL
)
''')
conn.commit()
conn.close()
print(f"Database created at {db_path} with table 'poll_stats'.")
