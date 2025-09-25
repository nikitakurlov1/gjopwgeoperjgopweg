import sqlite3
import json

def delete_comment(request, comment_id):
    try:
        # For this simple implementation, we'll simulate getting user_id from session
        # In a real app, this would come from the authenticated user's session
        user_id = 1  # Default user for testing
        
        # Connect to database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Verify that the user is the owner of the comment
        cursor.execute('''
            SELECT user_id FROM comments WHERE id = ?
        ''', (comment_id,))
        
        comment = cursor.fetchone()
        
        if not comment:
            conn.close()
            return json.dumps({
                'status': 'error',
                'message': 'Comment not found'
            }), 404
        
        if comment[0] != user_id:
            conn.close()
            return json.dumps({
                'status': 'error',
                'message': 'You are not authorized to delete this comment'
            }), 403
        
        # Delete the comment
        cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
        
        conn.commit()
        conn.close()
        
        # Return success response
        return json.dumps({
            'status': 'success',
            'message': 'Comment deleted successfully'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Error deleting comment: {str(e)}'
        }), 500