import sqlite3
import json
from flask import session

def get_comments(request, post_id):
    try:
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Fetch all comments for the specified post with author information
        cursor.execute('''
            SELECT 
                comments.id,
                comments.content,
                comments.created_at,
                users.first_name,
                users.last_name
            FROM comments 
            JOIN users ON comments.user_id = users.id
            WHERE comments.post_id = ?
            ORDER BY comments.created_at ASC
        ''', (post_id,))
        
        comments = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        comments_list = []
        for comment in comments:
            comments_list.append({
                'id': comment[0],
                'content': comment[1],
                'created_at': comment[2],
                'author_first_name': comment[3],
                'author_last_name': comment[4]
            })
        
        return json.dumps({
            'status': 'success',
            'data': comments_list
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Failed to fetch comments: {str(e)}'
        }), 500

def post_comment(request, post_id, socketio=None):
    try:
        # Check if user is logged in
        if 'user_id' not in session:
            return json.dumps({
                'status': 'error',
                'message': 'Необхідно увійти в систему'
            }), 401
            
        # Get user_id from session
        user_id = session['user_id']
        
        # Get JSON data from request
        data = request.get_json()
        content = data.get('content')
        
        # Validate required fields
        if not content:
            return json.dumps({
                'status': 'error',
                'message': 'Comment content is required'
            }), 400
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Insert new comment
        cursor.execute('''
            INSERT INTO comments (content, user_id, post_id)
            VALUES (?, ?, ?)
        ''', (content, user_id, post_id))
        
        # Get the ID of the newly inserted comment
        comment_id = cursor.lastrowid
        
        # Fetch the newly created comment with author information
        cursor.execute('''
            SELECT 
                comments.id,
                comments.content,
                comments.created_at,
                users.first_name,
                users.last_name
            FROM comments 
            JOIN users ON comments.user_id = users.id
            WHERE comments.id = ?
        ''', (comment_id,))
        
        comment = cursor.fetchone()
        conn.commit()
        conn.close()
        
        if comment:
            comment_data = {
                'id': comment[0],
                'content': comment[1],
                'created_at': comment[2],
                'author_first_name': comment[3],
                'author_last_name': comment[4],
                'post_id': post_id
            }
            
            # Emit WebSocket event for new comment
            if socketio:
                socketio.emit('new_comment', comment_data)
            
            return json.dumps({
                'status': 'success',
                'data': comment_data,
                'message': 'Comment posted successfully'
            }), 200
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Failed to retrieve created comment'
            }), 500
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Failed to process comment: {str(e)}'
        }), 500