import sqlite3
import hashlib

def create_admin_user():
    """
    Create an admin user with the hardcoded credentials for testing
    """
    # Connect to database
    conn = sqlite3.connect('messenger.db')
    cursor = conn.cursor()
    
    # Hash the admin password
    password_hash = hashlib.sha256('Zxcv1236'.encode()).hexdigest()
    
    # Insert admin user
    cursor.execute('''
        INSERT OR IGNORE INTO users 
        (first_name, last_name, class, category, school, phone, password_hash, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('Admin', 'User', 'Admin', 'Admin', 'Admin School', '0996055020', password_hash, 1))
    
    conn.commit()
    conn.close()
    
    print("Admin user created successfully!")

if __name__ == "__main__":
    create_admin_user()