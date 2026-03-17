import sqlite3
from embedding import add_embedding

conn = sqlite3.connect("memories.db")
cursor = conn.cursor()
cursor.execute("SELECT id, content FROM memories")
rows = cursor.fetchall()
conn.close()

for row in rows:
    memory_id = row[0]
    content = row[1]
    add_embedding(memory_id, content)
    print(f"Embedded memory {memory_id}: {content[:40]}...")

print("All memories embedded!")