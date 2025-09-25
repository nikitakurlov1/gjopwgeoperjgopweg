import sqlite3
import json

def get_posts(request):
    try:
        # For this simple implementation, we'll simulate getting user_id from session
        # In a real app, this would come from the authenticated user's session
        user_id = 1  # Default user for testing
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        conn.row_factory = sqlite3.Row  # This allows us to access columns by name
        cursor = conn.cursor()
        
        # Fetch all posts with author information and like counts
        cursor.execute('''
            SELECT 
                posts.id,
                posts.title,
                posts.content,
                posts.image_url,
                posts.category,
                posts.created_at,
                users.first_name,
                users.last_name,
                users.avatar_url,
                COALESCE(like_counts.like_count, 0) as like_count
            FROM posts 
            JOIN users ON posts.user_id = users.id
            LEFT JOIN (
                SELECT post_id, COUNT(*) as like_count
                FROM likes
                GROUP BY post_id
            ) like_counts ON posts.id = like_counts.post_id
            ORDER BY posts.created_at DESC
        ''')
        
        posts = cursor.fetchall()
        
        # Convert to list of dictionaries and add poll options for polls
        posts_list = []
        for post in posts:
            post_dict = {
                'id': post['id'],
                'title': post['title'],
                'content': post['content'],
                'image_url': post['image_url'],
                'category': post['category'],
                'created_at': post['created_at'],
                'author_first_name': post['first_name'],
                'author_last_name': post['last_name'],
                'author_avatar_url': post['avatar_url'],
                'like_count': post['like_count']
            }
            
            # If this is a poll, fetch the poll options and vote counts
            if post['category'] == 'Опитування':
                cursor.execute('''
                    SELECT 
                        po.id,
                        po.option_text,
                        COALESCE(vote_counts.vote_count, 0) as vote_count
                    FROM poll_options po
                    LEFT JOIN (
                        SELECT option_id, COUNT(*) as vote_count
                        FROM poll_votes
                        GROUP BY option_id
                    ) vote_counts ON po.id = vote_counts.option_id
                    WHERE po.post_id = ?
                    ORDER BY po.id
                ''', (post['id'],))
                
                poll_options = cursor.fetchall()
                post_dict['poll_options'] = []
                
                for option in poll_options:
                    # Check if current user has voted for this option
                    cursor.execute('''
                        SELECT id FROM poll_votes 
                        WHERE user_id = ? AND option_id = ?
                    ''', (user_id, option['id']))
                    
                    user_voted = cursor.fetchone() is not None
                    
                    post_dict['poll_options'].append({
                        'id': option['id'],
                        'option_text': option['option_text'],
                        'vote_count': option['vote_count'],
                        'user_voted': user_voted
                    })
                
                # Check if user has voted in this poll
                cursor.execute('''
                    SELECT id FROM poll_votes 
                    WHERE user_id = ? AND post_id = ?
                ''', (user_id, post['id']))
                
                post_dict['user_voted'] = cursor.fetchone() is not None
            
            posts_list.append(post_dict)
        
        conn.close()
        
        return json.dumps({
            'status': 'success',
            'data': posts_list
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка отримання постів: {str(e)}'
        }), 500