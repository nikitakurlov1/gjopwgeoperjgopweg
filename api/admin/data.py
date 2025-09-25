import sqlite3
import json
from flask import session

def get_admin_users(request):
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
        
        # Get all users
        cursor.execute('''
            SELECT id, first_name, last_name, phone, is_admin FROM users
        ''')
        
        users = cursor.fetchall()
        conn.close()
        
        # Format users data
        users_data = []
        for user in users:
            users_data.append({
                'id': user[0],
                'first_name': user[1],
                'last_name': user[2],
                'phone': user[3],
                'is_admin': bool(user[4])
            })
        
        return json.dumps({
            'status': 'success',
            'data': users_data
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка отримання даних: {str(e)}'
        }), 500

def get_admin_posts(request):
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
        
        # Get all posts with author information
        cursor.execute('''
            SELECT p.id, p.title, p.content, p.category, p.created_at, u.first_name, u.last_name
            FROM posts p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
        ''')
        
        posts = cursor.fetchall()
        conn.close()
        
        # Format posts data
        posts_data = []
        for post in posts:
            posts_data.append({
                'id': post[0],
                'title': post[1],
                'content': post[2],
                'category': post[3],
                'created_at': post[4],
                'author_first_name': post[5],
                'author_last_name': post[6]
            })
        
        return json.dumps({
            'status': 'success',
            'data': posts_data
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка отримання даних: {str(e)}'
        }), 500

def get_admin_comments(request):
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
        
        # Get all comments with author and post information
        cursor.execute('''
            SELECT c.id, c.content, c.created_at, u.first_name, u.last_name, p.title
            FROM comments c
            JOIN users u ON c.user_id = u.id
            JOIN posts p ON c.post_id = p.id
            ORDER BY c.created_at DESC
        ''')
        
        comments = cursor.fetchall()
        conn.close()
        
        # Format comments data
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment[0],
                'content': comment[1],
                'created_at': comment[2],
                'author_first_name': comment[3],
                'author_last_name': comment[4],
                'post_title': comment[5]
            })
        
        return json.dumps({
            'status': 'success',
            'data': comments_data
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка отримання даних: {str(e)}'
        }), 500