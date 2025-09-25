import sqlite3
import json

def vote_poll(request, post_id):
    try:
        # For this simple implementation, we'll simulate getting user_id from session
        # In a real app, this would come from the authenticated user's session
        user_id = 1  # Default user for testing
        
        # Get the selected option from the request
        data = request.get_json()
        option_id = data.get('option_id')
        
        # Validate input
        if not option_id:
            return json.dumps({
                'status': 'error',
                'message': 'Не вибрано варіант відповіді'
            }), 400
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Check if the user has already voted on this poll
        cursor.execute('''
            SELECT id FROM poll_votes 
            WHERE user_id = ? AND post_id = ?
        ''', (user_id, post_id))
        
        existing_vote = cursor.fetchone()
        
        if existing_vote:
            # Update existing vote
            cursor.execute('''
                UPDATE poll_votes 
                SET option_id = ? 
                WHERE user_id = ? AND post_id = ?
            ''', (option_id, user_id, post_id))
        else:
            # Insert new vote
            cursor.execute('''
                INSERT INTO poll_votes (user_id, option_id, post_id)
                VALUES (?, ?, ?)
            ''', (user_id, option_id, post_id))
        
        conn.commit()
        conn.close()
        
        # Return success response
        return json.dumps({
            'status': 'success',
            'message': 'Ваш голос зараховано!'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка голосування: {str(e)}'
        }), 500