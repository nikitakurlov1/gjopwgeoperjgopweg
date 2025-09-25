import sqlite3
import json

def delete_post(request, post_id):
    try:
        # For this simple implementation, we'll simulate getting user_id from session
        # In a real app, this would come from the authenticated user's session
        user_id = 1  # Default user for testing
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Verify that the user is the owner of the post
        cursor.execute('''
            SELECT user_id FROM posts WHERE id = ?
        ''', (post_id,))
        
        post = cursor.fetchone()
        
        if not post:
            conn.close()
            return json.dumps({
                'status': 'error',
                'message': 'Post not found'
            }), 404
        
        if post[0] != user_id:
            conn.close()
            return json.dumps({
                'status': 'error',
                'message': 'You are not authorized to delete this post'
            }), 403
        
        # Perform cascading deletes
        # Delete likes for the post
        cursor.execute('DELETE FROM likes WHERE post_id = ?', (post_id,))
        
        # Delete comments for the post
        cursor.execute('DELETE FROM comments WHERE post_id = ?', (post_id,))
        
        # Delete poll options for the post (if any)
        cursor.execute('DELETE FROM poll_options WHERE post_id = ?', (post_id,))
        
        # Delete poll votes for the post (if any)
        cursor.execute('DELETE FROM poll_votes WHERE post_id = ?', (post_id,))
        
        # Delete the post itself
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        
        conn.commit()
        conn.close()
        
        # Return success response
        return json.dumps({
            'status': 'success',
            'message': 'Post deleted successfully'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Error deleting post: {str(e)}'
        }), 500