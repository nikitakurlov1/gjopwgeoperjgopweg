import sqlite3
import json
from flask import session

def get_conversations(request):
    # Check if user is admin
    if not session.get('is_admin'):
        return json.dumps({
            'status': 'error',
            'message': 'Доступ заборонено'
        }), 403
    
    try:
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Get unique users who have sent messages
        cursor.execute('''
            SELECT DISTINCT u.id, u.first_name, u.last_name
            FROM trust_box_messages t
            JOIN users u ON t.user_id = u.id
            ORDER BY u.first_name, u.last_name
        ''')
        
        users = cursor.fetchall()
        conn.close()
        
        # Format users data
        users_data = []
        for user in users:
            users_data.append({
                'id': user[0],
                'first_name': user[1],
                'last_name': user[2]
            })
        
        return json.dumps({
            'status': 'success',
            'data': users_data
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка отримання списку розмов: {str(e)}'
        }), 500

def get_conversation(request, user_id):
    # Check if user is admin
    if not session.get('is_admin'):
        return json.dumps({
            'status': 'error',
            'message': 'Доступ заборонено'
        }), 403
    
    try:
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Get message history for this user
        cursor.execute('''
            SELECT t.id, t.message_text, t.sent_by_admin, t.timestamp, u.first_name, u.last_name
            FROM trust_box_messages t
            JOIN users u ON t.user_id = u.id
            WHERE t.user_id = ?
            ORDER BY t.timestamp ASC
        ''', (user_id,))
        
        messages = cursor.fetchall()
        conn.close()
        
        # Format messages data
        messages_data = []
        for message in messages:
            messages_data.append({
                'id': message[0],
                'message_text': message[1],
                'sent_by_admin': bool(message[2]),
                'timestamp': message[3],
                'first_name': message[4],
                'last_name': message[5]
            })
        
        return json.dumps({
            'status': 'success',
            'data': messages_data
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка отримання історії розмови: {str(e)}'
        }), 500

def send_reply(request, user_id, socketio=None):
    # Check if user is admin
    if not session.get('is_admin'):
        return json.dumps({
            'status': 'error',
            'message': 'Доступ заборонено'
        }), 403
    
    try:
        # Get JSON data from request
        data = request.get_json()
        message_text = data.get('message_text')
        
        # Validate required fields
        if not message_text:
            return json.dumps({
                'status': 'error',
                'message': 'Повідомлення не може бути порожнім'
            }), 400
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Insert new message from admin
        cursor.execute('''
            INSERT INTO trust_box_messages (user_id, message_text, sent_by_admin)
            VALUES (?, ?, ?)
        ''', (user_id, message_text, True))
        
        # Get the ID of the newly inserted message
        message_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        # Emit WebSocket event for new private message
        if socketio:
            # Fetch the newly created message with author information
            conn = sqlite3.connect('messenger.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.id, t.message_text, t.sent_by_admin, t.timestamp, u.first_name, u.last_name
                FROM trust_box_messages t
                JOIN users u ON t.user_id = u.id
                WHERE t.id = ?
            ''', (message_id,))
            
            message = cursor.fetchone()
            conn.close()
            
            if message:
                message_data = {
                    'id': message[0],
                    'message_text': message[1],
                    'sent_by_admin': bool(message[2]),
                    'timestamp': message[3],
                    'first_name': message[4],
                    'last_name': message[5],
                    'user_id': user_id
                }
                # Emit to the specific user's room
                socketio.emit('private_message', message_data, room=str(user_id))
        
        return json.dumps({
            'status': 'success',
            'message': 'Відповідь відправлено'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка відправки відповіді: {str(e)}'
        }), 500