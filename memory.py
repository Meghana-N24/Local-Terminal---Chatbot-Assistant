import sqlite3
import datetime

# The name of our database file
# This file will be created automatically


DB_FILE = "terminal_memory.db"


# FUNCTION 1: Initialize the database
# Creates tables if they don't exist yet
# Run this once when assistant starts

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Table 1: stores every command run
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS command_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            had_error INTEGER,
            timestamp TEXT
        )
    """)

    # Table 2: stores every error seen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            error TEXT,
            fix TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Memory system ready.")



# FUNCTION 2: Save a command to history
# had_error = 1 means yes, 0 means no


def save_command(command, had_error):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO command_history (command, had_error, timestamp)
        VALUES (?, ?, ?)
    """, (command, had_error, timestamp))

    conn.commit()
    conn.close()


# FUNCTION 3: Save an error + its fix

def save_error(command, error, fix):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO error_history (command, error, fix, timestamp)
        VALUES (?, ?, ?, ?)
    """, (command, error, fix, timestamp))

    conn.commit()
    conn.close()


# FUNCTION 4: Search for similar past errors
# Looks for keywords from current error
# Returns last 3 matches

def find_similar_errors(error_text):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Take first 30 characters as search keyword
    keyword = error_text[:30]

    cursor.execute("""
        SELECT command, error, fix, timestamp
        FROM error_history
        WHERE error LIKE ?
        ORDER BY timestamp DESC
        LIMIT 3
    """, (f"%{keyword}%",))

    rows = cursor.fetchall()
    conn.close()
    return rows


# FUNCTION 5: Get recent command history
# Returns last 5 commands run

def get_recent_history(limit=5):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT command, had_error, timestamp
        FROM command_history
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows



# FUNCTION 6: Count  how many times an
# error has been seen before

def count_error_occurrences(error_text):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    keyword = error_text[:30]

    cursor.execute("""
        SELECT COUNT(*)
        FROM error_history
        WHERE error LIKE ?
    """, (f"%{keyword}%",))

    count = cursor.fetchone()[0]
    conn.close()
    return count
