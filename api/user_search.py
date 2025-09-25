import sqlite3
import json

def search_users(request):
    try:
        # Get search query parameter
        search_query = request.args.get('q', '')
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Search users based on first_name or last_name
        if search_query:
            cursor.execute('''
                SELECT id, first_name, last_name, avatar_url
                FROM users
                WHERE first_name LIKE ? OR last_name LIKE ?
                ORDER BY first_name, last_name
            ''', (f'%{search_query}%', f'%{search_query}%'))
        else:
            # If no search query, return all users
            cursor.execute('''
                SELECT id, first_name, last_name, avatar_url
                FROM users
                ORDER BY first_name, last_name
            ''')
        
        users = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        users_list = []
        for user in users:
            users_list.append({
                'id': user['id'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'avatar_url': user['avatar_url'] if user['avatar_url'] else 'static/default-avatar.svg'
            })
        
        return json.dumps({
            'status': 'success',
            'data': users_list
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Error searching users: {str(e)}'
        }), 500