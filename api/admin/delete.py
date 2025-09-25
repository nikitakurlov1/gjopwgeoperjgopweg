import sqlite3
import json
from flask import session

def delete_user(request, user_id):
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
        
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return json.dumps({
                'status': 'error',
                'message': 'Користувача не знайдено'
            }), 404
        
        # Delete user and all related data
        # Delete user's comments
        cursor.execute('DELETE FROM comments WHERE user_id = ?', (user_id,))
        
        # Delete user's likes
        cursor.execute('DELETE FROM likes WHERE user_id = ?', (user_id,))
        
        # Delete user's posts (and their comments will be deleted by cascade)
        cursor.execute('DELETE FROM posts WHERE user_id = ?', (user_id,))
        
        # Delete the user
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return json.dumps({
            'status': 'success',
            'message': 'Користувача видалено'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка видалення: {str(e)}'
        }), 500

def delete_post(request, post_id):
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
        
        # Check if post exists
        cursor.execute('SELECT id FROM posts WHERE id = ?', (post_id,))
        post = cursor.fetchone()
        
        if not post:
            conn.close()
            return json.dumps({
                'status': 'error',
                'message': 'Пост не знайдено'
            }), 404
        
        # Delete post and all related comments
        cursor.execute('DELETE FROM comments WHERE post_id = ?', (post_id,))
        cursor.execute('DELETE FROM likes WHERE post_id = ?', (post_id,))
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        
        conn.commit()
        conn.close()
        
        return json.dumps({
            'status': 'success',
            'message': 'Пост видалено'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка видалення: {str(e)}'
        }), 500

def delete_comment(request, comment_id):
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
        
        # Check if comment exists
        cursor.execute('SELECT id FROM comments WHERE id = ?', (comment_id,))
        comment = cursor.fetchone()
        
        if not comment:
            conn.close()
            return json.dumps({
                'status': 'error',
                'message': 'Коментар не знайдено'
            }), 404
        
        # Delete the comment
        cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
        
        conn.commit()
        conn.close()
        
        return json.dumps({
            'status': 'success',
            'message': 'Коментар видалено'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка видалення: {str(e)}'
        }), 500