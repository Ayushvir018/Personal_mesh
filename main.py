import sqlite3

def add_memory(content, user_id, mem_type, priority):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO memories (content, user_id, type, priority) VALUES (?, ?, ?, ?)",
        (content, user_id, mem_type, priority)
    )
    conn.commit()
    conn.close()
    print("Memory saved.")

def view_all_memories():
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memories ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    for row in rows:
        print(f"[{row[0]}] {row[1]} | {row[4]} | {row[5]} | {row[2]}")
    conn.close()

def filter_by_type(mem_type):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM memories WHERE type = ? ORDER BY timestamp DESC",
        (mem_type,)
    )
    rows = cursor.fetchall()
    for row in rows:
        print(f"[{row[0]}] {row[1]} | {row[4]} | {row[5]} | {row[2]}")
    conn.close()

def search_memory(keyword):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM memories WHERE content LIKE ?",
        ('%' + keyword + '%',)
    )
    rows = cursor.fetchall()
    for row in rows:
        print(f"[{row[0]}] {row[1]} | {row[4]} | {row[5]} | {row[2]}")
    conn.close()

def filter_by_date(date):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM memories WHERE DATE(timestamp) = ?",
        (date,)
    )
    rows = cursor.fetchall()
    for row in rows:
        print(f"[{row[0]}] {row[1]} | {row[4]} | {row[5]} | {row[2]}")
    conn.close()

# ALL calls here at the bottom
filter_by_date("2026-03-16")