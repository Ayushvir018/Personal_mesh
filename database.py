import sqlite3

def create_db():
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id TEXT,
            type TEXT,
            priority TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database ready.")

create_db()