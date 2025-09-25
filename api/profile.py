import sqlite3
import json
from flask import session

def calculate_stars(posts_count, likes_received, comments_received):
    """
    Calculate user's reputation stars based on the business logic:
    - 10 stars for each post created
    - 1 star for each like received on posts
    - 2 stars for each comment received on posts
    """
    return (posts_count * 10) + likes_received + (comments_received * 2)

def get_user_profile(request):
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
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get user information
        cursor.execute('''
            SELECT id, first_name, last_name, avatar_url
            FROM users
            WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            return json.dumps({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        # Get statistics
        # Posts created
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM posts
            WHERE user_id = ?
        ''', (user_id,))
        posts_created = cursor.fetchone()['count']
        
        # Likes received on posts
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM likes l
            JOIN posts p ON l.post_id = p.id
            WHERE p.user_id = ?
        ''', (user_id,))
        likes_received = cursor.fetchone()['count']
        
        # Comments received on posts
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM comments c
            JOIN posts p ON c.post_id = p.id
            WHERE p.user_id = ?
        ''', (user_id,))
        comments_received = cursor.fetchone()['count']
        
        # Comments made by user
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM comments
            WHERE user_id = ?
        ''', (user_id,))
        comments_made = cursor.fetchone()['count']
        
        # Likes given by user
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM likes
            WHERE user_id = ?
        ''', (user_id,))
        likes_given = cursor.fetchone()['count']
        
        # Calculate stars
        total_stars = calculate_stars(posts_created, likes_received, comments_received)
        
        # Get user's posts
        cursor.execute('''
            SELECT 
                p.id,
                p.title,
                p.content,
                p.category,
                p.created_at,
                COALESCE(like_counts.like_count, 0) as like_count
            FROM posts p
            LEFT JOIN (
                SELECT post_id, COUNT(*) as like_count
                FROM likes
                GROUP BY post_id
            ) like_counts ON p.id = like_counts.post_id
            WHERE p.user_id = ?
            ORDER BY p.created_at DESC
        ''', (user_id,))
        
        posts = cursor.fetchall()
        user_posts = []
        for post in posts:
            user_posts.append({
                'id': post['id'],
                'title': post['title'],
                'content': post['content'],
                'category': post['category'],
                'created_at': post['created_at'],
                'like_count': post['like_count']
            })
        
        # Get user's comments with post information
        cursor.execute('''
            SELECT 
                c.id,
                c.content,
                c.created_at,
                p.id as post_id,
                p.title as post_title
            FROM comments c
            JOIN posts p ON c.post_id = p.id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
        ''', (user_id,))
        
        comments = cursor.fetchall()
        user_comments = []
        for comment in comments:
            user_comments.append({
                'id': comment['id'],
                'content': comment['content'],
                'created_at': comment['created_at'],
                'post_id': comment['post_id'],
                'post_title': comment['post_title']
            })
        
        conn.close()
        
        # Prepare response
        response_data = {
            'user_info': {
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'avatar_url': user['avatar_url'] if user['avatar_url'] else 'static/default-avatar.svg'
            },
            'statistics': {
                'posts_created': posts_created,
                'likes_received': likes_received,
                'comments_made': comments_made,
                'likes_given': likes_given,
                'total_stars': total_stars
            },
            'user_posts': user_posts,
            'user_comments': user_comments
        }
        
        return json.dumps({
            'status': 'success',
            'data': response_data
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Error fetching profile: {str(e)}'
        }), 500