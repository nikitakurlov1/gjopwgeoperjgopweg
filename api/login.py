import sqlite3
import hashlib
import json
from flask import session

def login_user(request):
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Extract fields
        phone = data.get('phone')
        password = data.get('password')
        
        # Validate required fields
        if not phone or not password:
            return json.dumps({
                'status': 'error',
                'message': 'Номер телефону та пароль обов\'язкові'
            }), 400
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Find user by phone number and verify password
        cursor.execute('''
            SELECT id, is_admin FROM users WHERE phone = ? AND password_hash = ?
        ''', (phone, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_id, is_admin = user
            
            # Check if this is the superuser
            if phone == '0996055020' and password_hash == hashlib.sha256('Zxcv1236'.encode()).hexdigest():
                # Set admin session
                session['user_id'] = user_id
                session['is_admin'] = True
                return json.dumps({
                    'status': 'redirect',
                    'url': '/admin.html'
                }), 200
            else:
                # Regular user login
                session['user_id'] = user_id
                session['is_admin'] = is_admin
                return json.dumps({
                    'status': 'redirect',
                    'url': '/lenta.html'
                }), 200
        else:
            # Invalid credentials
            return json.dumps({
                'status': 'error',
                'message': 'Невірний номер телефону або пароль'
            }), 401
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка входу: {str(e)}'
        }), 500