import sqlite3
import json
import os
from werkzeug.utils import secure_filename
from flask import session

def update_avatar(request):
    try:
        # Get user_id from session
        if 'user_id' not in session:
            return json.dumps({
                'status': 'error',
                'message': 'Необхідно увійти в систему'
            }), 401
        user_id = session['user_id']
        
        # Check if file is present in request
        if 'avatar' not in request.files:
            return json.dumps({
                'status': 'error',
                'message': 'No file provided'
            }), 400
        
        file = request.files['avatar']
        
        # Check if file is selected
        if file.filename == '':
            return json.dumps({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        # Validate file type (simple check)
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return json.dumps({
                'status': 'error',
                'message': 'Invalid file type. Please upload an image file.'
            }), 400
        
        # Create avatars directory if it doesn't exist
        avatars_dir = 'static/avatars'
        if not os.path.exists(avatars_dir):
            os.makedirs(avatars_dir)
        
        # Secure the filename and save the file
        filename = secure_filename(f"user_{user_id}_{file.filename}")
        file_path = os.path.join(avatars_dir, filename)
        file.save(file_path)
        
        # Update user's avatar URL in database
        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()
        
        # Update avatar_url for the user
        cursor.execute('''
            UPDATE users
            SET avatar_url = ?
            WHERE id = ?
        ''', (file_path, user_id))
        
        conn.commit()
        conn.close()
        
        # Return success response
        return json.dumps({
            'status': 'success',
            'message': 'Avatar updated successfully',
            'new_avatar_url': file_path
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Error updating avatar: {str(e)}'
        }), 500