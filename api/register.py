import sqlite3
import hashlib
import json
from flask import session

def register_user(request):
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Extract fields
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_class = data.get('class')
        category = data.get('category')
        school = data.get('school')
        phone = data.get('phone')
        password = data.get('password')
        
        # Validate required fields
        if not all([first_name, last_name, category, school, phone, password]):
            return json.dumps({
                'status': 'error',
                'message': 'Всі обов\'язкові поля повинні бути заповнені'
            }), 400
        
        # Validate password length
        if len(password) < 8:
            return json.dumps({
                'status': 'error',
                'message': 'Пароль має містити мінімум 8 символів'
            }), 400
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Check if phone number already exists
        cursor.execute('SELECT id FROM users WHERE phone = ?', (phone,))
        if cursor.fetchone():
            conn.close()
            return json.dumps({
                'status': 'error',
                'message': 'Користувач з таким номером телефону вже існує'
            }), 400
        
        # Insert new user
        cursor.execute('''
            INSERT INTO users (first_name, last_name, class, category, school, phone, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, user_class, category, school, phone, password_hash))
        
        # Get the ID of the newly inserted user
        new_user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        # Set session for the newly registered user
        session['user_id'] = new_user_id
        session['is_admin'] = False  # New users are not admins by default
        
        # Return success response with redirect
        return json.dumps({
            'status': 'redirect',
            'url': '/lenta.html'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка реєстрації: {str(e)}'
        }), 500