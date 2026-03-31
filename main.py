import sqlite3

def add_memory(content, user_id, mem_type, priority, date=None):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    
    if date:
        cursor.execute(
            "INSERT INTO memories (content, timestamp, user_id, type, priority) VALUES (?, ?, ?, ?, ?)",
            (content, date, user_id, mem_type, priority)
        )
    else:
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

def edit_memory(memory_id, new_content):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE memories SET content = ? WHERE id = ?",
        (new_content, memory_id)
    )
    conn.commit()
    conn.close()
    print("Memory updated.")


def delete_memory(memory_id):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM memories WHERE id = ?",
        (memory_id,)
    )
    conn.commit()
    conn.close()
    print("Memory deleted.")


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
def menu():
    while True:
        print("\n=== Personal Mesh Memory System ===")
        print("1. Add new memory")
        print("2. View all memories")
        print("3. Filter by type")
        print("4. Search memories")
        print("5. Filter by date")
        print("6. Delete memory")
        print("7. Edit memory")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            content = input("Enter what happened: ")
            user_id = input("Enter user id (press Enter for 'ayush'): ") or "ayush"
            mem_type = input("Enter type (project/personal/health/work): ")
            priority = input("Enter priority (low/medium/high): ") or "medium"
            date = input("Enter date (YYYY-MM-DD, press Enter for today): ") or None
            add_memory(content, user_id, mem_type, priority, date)

        elif choice == "2":
            view_all_memories()

        elif choice == "3":
            mem_type = input("Enter type to filter (project/personal/health/work): ")
            filter_by_type(mem_type)

        elif choice == "4":
            keyword = input("Enter keyword to search: ")
            search_memory(keyword)

        elif choice == "5":
            date = input("Enter date (YYYY-MM-DD): ")
            filter_by_date(date)

        elif choice == "6":
            view_all_memories()
            memory_id = input("Enter memory ID to delete: ")
            delete_memory(memory_id)
    
        elif choice == "7":
            view_all_memories()
            memory_id = input("Enter memory ID to edit: ")
            new_content = input("Enter new content: ")
            edit_memory(memory_id, new_content)

        elif choice == "8":
            print("Goodbye! Your memories are safely saved.")
            break   
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
menu()
