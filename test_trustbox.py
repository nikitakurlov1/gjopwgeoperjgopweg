import sqlite3

def test_trustbox_setup():
    """
    Test the trust box database setup
    """
    # Connect to database
    conn = sqlite3.connect('messenger.db')
    cursor = conn.cursor()
    
    # Check if trust_box_messages table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trust_box_messages'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print("Trust Box table exists!")
        
        # Test inserting a message
        cursor.execute('''
            INSERT INTO trust_box_messages (user_id, message_text, sent_by_admin)
            VALUES (?, ?, ?)
        ''', (1, 'Test message from student', False))
        
        cursor.execute('''
            INSERT INTO trust_box_messages (user_id, message_text, sent_by_admin)
            VALUES (?, ?, ?)
        ''', (1, 'Test reply from admin', True))
        
        conn.commit()
        print("Test messages inserted successfully!")
        
        # Test retrieving messages
        cursor.execute('''
            SELECT t.id, t.message_text, t.sent_by_admin, t.timestamp, u.first_name, u.last_name
            FROM trust_box_messages t
            JOIN users u ON t.user_id = u.id
            WHERE t.user_id = ?
            ORDER BY t.timestamp ASC
        ''', (1,))
        
        messages = cursor.fetchall()
        print(f"Retrieved {len(messages)} messages:")
        for message in messages:
            sender = "Admin" if message[2] else "Student"
            print(f"  {sender}: {message[1]}")
    else:
        print("Trust Box table does not exist!")
    
    conn.close()

if __name__ == "__main__":
    test_trustbox_setup()