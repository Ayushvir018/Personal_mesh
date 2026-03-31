import sqlite3
from embedding import add_embedding

conn = sqlite3.connect("memories.db")
cursor = conn.cursor()
# Fetch ID, content, and user_id for correct metadata tagging
cursor.execute("SELECT id, content, user_id FROM memories")
rows = cursor.fetchall()
conn.close()

for row in rows:
    memory_id = row[0]
    content = row[1]
    user_id = row[2]
    add_embedding(memory_id, content, user_id)
    print(f"Embedded memory {memory_id} (User: {user_id}): {content[:40]}...")

print("All memories embedded with user metadata!")