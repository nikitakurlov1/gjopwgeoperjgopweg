import sqlite3
import json
from flask import session

def send_message(request, socketio=None):
    try:
        # Check if user is logged in
        if 'user_id' not in session:
            return json.dumps({
                'status': 'error',
                'message': 'Необхідно увійти в систему'
            }), 401
        
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
        
        # Insert new message
        cursor.execute('''
            INSERT INTO trust_box_messages (user_id, message_text, sent_by_admin)
            VALUES (?, ?, ?)
        ''', (session['user_id'], message_text, False))
        
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
                    'user_id': session['user_id']
                }
                # Emit to the specific user's room
                socketio.emit('private_message', message_data, room=str(session['user_id']))
        
        return json.dumps({
            'status': 'success',
            'message': 'Повідомлення відправлено'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка відправки повідомлення: {str(e)}'
        }), 500

def get_message_history(request):
    try:
        # Check if user is logged in
        if 'user_id' not in session:
            return json.dumps({
                'status': 'error',
                'message': 'Необхідно увійти в систему'
            }), 401
        
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
        ''', (session['user_id'],))
        
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
            'message': f'Помилка отримання історії повідомлень: {str(e)}'
        }), 500