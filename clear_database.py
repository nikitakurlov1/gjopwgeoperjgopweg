import sqlite3
import os

def clear_database():
    # Connect to the database
    conn = sqlite3.connect('messenger.db')
    cursor = conn.cursor()
    
    # Delete all records from all tables
    tables = ['trust_box_messages', 'comments', 'likes', 'posts', 'users']
    
    for table in tables:
        try:
            cursor.execute(f'DELETE FROM {table}')
            print(f"Cleared all records from {table}")
        except sqlite3.Error as e:
            print(f"Error clearing {table}: {e}")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database cleared successfully!")

if __name__ == "__main__":
    # Confirm with user before proceeding
    confirm = input("This will delete all posts and accounts. Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        clear_database()
    else:
        print("Operation cancelled.")