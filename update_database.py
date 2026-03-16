import sqlite3

conn = sqlite3.connect("memories.db")
cursor = conn.cursor()

# Add tags column
cursor.execute("ALTER TABLE memories ADD COLUMN tags TEXT DEFAULT ''")

conn.commit()
conn.close()

print("✅ Database updated with tags column!")