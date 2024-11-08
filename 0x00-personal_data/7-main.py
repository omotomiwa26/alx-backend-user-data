#!/usr/bin/env python3
"""
Main file
"""
try:

    get_db = __import__('filtered_logger').get_db

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    for row in cursor:
        print(row[0])
    cursor.close()
    db.close()

except Exception as e:
    print(f"Error: {e}")