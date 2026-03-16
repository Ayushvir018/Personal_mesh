import sqlite3
from datetime import datetime

def add_memory(content, user_id="ayush", mem_type="personal", priority="medium", date=None, tags=""):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    
    if date:
        cursor.execute(
            "INSERT INTO memories (content, timestamp, user_id, type, priority, tags) VALUES (?, ?, ?, ?, ?, ?)",
            (content, date, user_id, mem_type, priority, tags)
        )
    else:
        cursor.execute(
            "INSERT INTO memories (content, user_id, type, priority, tags) VALUES (?, ?, ?, ?, ?)",
            (content, user_id, mem_type, priority, tags)
        )
    
    conn.commit()
    conn.close()
    return "✅ Memory saved successfully!"


def get_all_memories():
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memories ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def filter_by_type(mem_type):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM memories WHERE type = ? ORDER BY timestamp DESC",
        (mem_type,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_memory(keyword):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM memories WHERE content LIKE ? ORDER BY timestamp DESC",
        ('%' + keyword + '%',)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def filter_by_date(date):
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM memories WHERE DATE(timestamp) = ? ORDER BY timestamp DESC",
        (date,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_memory(memory_id):
    try:
        conn = sqlite3.connect("memories.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memories WHERE id = ?", (int(memory_id),))
        conn.commit()
        conn.close()
        return "✅ Memory deleted successfully!"
    except:
        return "❌ Error: Invalid ID"


def edit_memory(memory_id, new_content):
    try:
        conn = sqlite3.connect("memories.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE memories SET content = ? WHERE id = ?",
            (new_content, int(memory_id))
        )
        conn.commit()
        conn.close()
        return "✅ Memory updated successfully!"
    except:
        return "❌ Error: Invalid ID"
def get_stats():
    """Get overall statistics"""
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    
    # Total count
    cursor.execute("SELECT COUNT(*) FROM memories")
    total = cursor.fetchone()[0]
    
    # Count by type
    cursor.execute("SELECT type, COUNT(*) FROM memories GROUP BY type")
    by_type = cursor.fetchall()
    
    # Count by priority
    cursor.execute("SELECT priority, COUNT(*) FROM memories GROUP BY priority")
    by_priority = cursor.fetchall()
    
    # Recent memories (last 7 days)
    cursor.execute("""
        SELECT DATE(timestamp), COUNT(*) 
        FROM memories 
        WHERE DATE(timestamp) >= DATE('now', '-7 days')
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
    """)
    recent = cursor.fetchall()
    
    conn.close()
    
    return {
        'total': total,
        'by_type': by_type,
        'by_priority': by_priority,
        'recent': recent
    }

def search_by_tag(tag):
    """Search memories by tag"""
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM memories WHERE tags LIKE ? ORDER BY timestamp DESC",
        ('%' + tag + '%',)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_tags():
    """Get all unique tags"""
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tags FROM memories WHERE tags != ''")
    rows = cursor.fetchall()
    conn.close()
    
    # Extract unique tags
    all_tags = []
    for row in rows:
        if row[0]:
            tags = [t.strip() for t in row[0].split(',')]
            all_tags.extend(tags)
    
    return list(set(all_tags))  # unique tags only