import sqlite3
import json
from flask import session

def toggle_like(request, post_id, socketio=None):
    try:
        # Check if user is logged in
        if 'user_id' not in session:
            return json.dumps({
                'status': 'error',
                'message': 'Необхідно увійти в систему'
            }), 401
            
        # Get user_id from session
        user_id = session['user_id']
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Check if the user has already liked this post
        cursor.execute('''
            SELECT id FROM likes WHERE user_id = ? AND post_id = ?
        ''', (user_id, post_id))
        
        existing_like = cursor.fetchone()
        
        if existing_like:
            # Unlike: Remove the like
            cursor.execute('''
                DELETE FROM likes WHERE user_id = ? AND post_id = ?
            ''', (user_id, post_id))
            liked_by_user = False
        else:
            # Like: Add a new like
            cursor.execute('''
                INSERT INTO likes (user_id, post_id) VALUES (?, ?)
            ''', (user_id, post_id))
            liked_by_user = True
        
        # Get the new like count
        cursor.execute('''
            SELECT COUNT(*) FROM likes WHERE post_id = ?
        ''', (post_id,))
        
        new_like_count = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        # Emit WebSocket event for post update
        if socketio:
            socketio.emit('post_update', {
                'post_id': post_id,
                'new_like_count': new_like_count
            })
        
        return json.dumps({
            'status': 'success',
            'data': {
                'liked_by_user': liked_by_user,
                'new_like_count': new_like_count
            },
            'message': 'Like added/removed successfully'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Post not found or action failed: {str(e)}'
        }), 500