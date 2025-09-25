from flask import Flask, request, jsonify, redirect, url_for, send_from_directory, session
import sqlite3
import hashlib
import os

# Import SocketIO
from flask_socketio import SocketIO, emit

# Import API endpoints
from api.register import register_user
from api.login import login_user
from api.logout import logout_user
from api.posts import get_posts
from api.create_post import create_post
from api.like_post import toggle_like
from api.comments import get_comments, post_comment
from api.vote_poll import vote_poll
from api.profile import get_user_profile
from api.avatar import update_avatar
from api.delete_post import delete_post
from api.delete_comment import delete_comment
from api.user_search import search_users
from api.public_profile import get_public_profile
# Import admin API endpoints
from api.admin.data import get_admin_users, get_admin_posts, get_admin_comments
from api.admin.delete import delete_user, delete_post as admin_delete_post, delete_comment as admin_delete_comment
# Import trust box API endpoints
from api.trustbox import send_message, get_message_history
from api.admin_trustbox import get_conversations, get_conversation, send_reply

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Initialize database
def init_db():
    # Ensure the database file is in the correct location
    db_path = os.environ.get('DATABASE_URL', 'messenger.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            class TEXT,
            category TEXT NOT NULL,
            school TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0,
            avatar_url TEXT NOT NULL DEFAULT 'static/avatars/default-avatar.svg'
        )
    ''')
    
    # Create posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image_url TEXT,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create likes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (post_id) REFERENCES posts (id),
            UNIQUE(user_id, post_id)
        )
    ''')
    
    # Create comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    ''')
    
    # Create trust_box_messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trust_box_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            sent_by_admin BOOLEAN NOT NULL DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Check if columns exist, add them if not
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN avatar_url TEXT NOT NULL DEFAULT 'static/avatars/default-avatar.svg'")
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# API routes
@app.route('/api/register', methods=['POST'])
def register():
    return register_user(request)

@app.route('/api/login', methods=['POST'])
def login():
    return login_user(request)

@app.route('/api/logout', methods=['POST'])
def logout():
    return logout_user(request)

@app.route('/api/posts', methods=['GET'])
def posts():
    return get_posts(request)

@app.route('/api/create_post', methods=['POST'])
def create_post_route():
    return create_post(request, socketio)  # Pass socketio to the function

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    return toggle_like(request, post_id, socketio)  # Pass socketio to the function

@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def comments_get(post_id):
    return get_comments(request, post_id)

@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def comments_post(post_id):
    return post_comment(request, post_id, socketio)  # Pass socketio to the function

@app.route('/api/posts/<int:post_id>/vote', methods=['POST'])
def vote_poll_route(post_id):
    return vote_poll(request, post_id)

@app.route('/api/profile', methods=['GET'])
def profile():
    return get_user_profile(request)

@app.route('/api/profile/avatar', methods=['POST'])
def avatar():
    return update_avatar(request)

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post_route(post_id):
    return delete_post(request, post_id)

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment_route(comment_id):
    return delete_comment(request, comment_id)

@app.route('/api/users/search', methods=['GET'])
def user_search():
    return search_users(request)

@app.route('/api/user/<int:user_id>/profile', methods=['GET'])
def public_profile(user_id):
    return get_public_profile(request, user_id)

# Admin API routes
@app.route('/api/admin/users', methods=['GET'])
def admin_users():
    return get_admin_users(request)

@app.route('/api/admin/posts', methods=['GET'])
def admin_posts():
    return get_admin_posts(request)

@app.route('/api/admin/comments', methods=['GET'])
def admin_comments():
    return get_admin_comments(request)

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    return delete_user(request, user_id)

@app.route('/api/admin/posts/<int:post_id>', methods=['DELETE'])
def admin_delete_post_route(post_id):
    return admin_delete_post(request, post_id)

@app.route('/api/admin/comments/<int:comment_id>', methods=['DELETE'])
def admin_delete_comment_route(comment_id):
    return admin_delete_comment(request, comment_id)

# Trust Box API routes for students
@app.route('/api/trustbox/message', methods=['POST'])
def trustbox_message():
    return send_message(request, socketio)  # Pass socketio to the function

@app.route('/api/trustbox/history', methods=['GET'])
def trustbox_history():
    return get_message_history(request)

# Trust Box API routes for admin
@app.route('/api/admin/trustbox/conversations', methods=['GET'])
def admin_trustbox_conversations():
    return get_conversations(request)

@app.route('/api/admin/trustbox/conversation/<int:user_id>', methods=['GET'])
def admin_trustbox_conversation(user_id):
    return get_conversation(request, user_id)

@app.route('/api/admin/trustbox/reply/<int:user_id>', methods=['POST'])
def admin_trustbox_reply(user_id):
    return send_reply(request, user_id, socketio)  # Pass socketio to the function

# Serve static files
@app.route('/')
def index():
    return redirect('/static/index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Get the port from the environment variable, default to 5000 if not set
    port = int(os.environ.get('PORT', 5000))
    
    # Check if we're running in a production environment
    if os.environ.get('FLASK_ENV') == 'production':
        # For production, run without debug mode and with allow_unsafe_werkzeug
        socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
    else:
        # Development environment
        socketio.run(app, debug=True, port=port)