import sqlite3

def create_db():
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create memories table with all columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id TEXT,
            type TEXT,
            priority TEXT,
            tags TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()
    print("Database ready.")

if __name__ == "__main__":
    create_db()