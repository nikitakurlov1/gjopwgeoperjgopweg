import sqlite3
import json
import os
from flask import session
from werkzeug.utils import secure_filename

def create_post(request, socketio=None):
    try:
        if 'user_id' not in session:
            return json.dumps({'status': 'error', 'message': 'Необхідно увійти в систему'}), 401

        user_id = session['user_id']
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        poll_options = request.form.getlist('poll_options[]')

        if not all([title, content, category]):
            return json.dumps({'status': 'error', 'message': 'Всі обов\'язкові поля повинні бути заповнені'}), 400

        if category == 'Опитування' and (not poll_options or not any(option.strip() for option in poll_options)):
            return json.dumps({'status': 'error', 'message': 'Для опитування потрібно додати хоча б один варіант відповіді'}), 400

        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                images_dir = 'static/post_images'
                if not os.path.exists(images_dir):
                    os.makedirs(images_dir)
                filename = secure_filename(f"post_{user_id}_{file.filename}")
                file_path = os.path.join(images_dir, filename)
                file.save(file_path)
                image_url = file_path

        conn = sqlite3.connect('messenger.db')
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO posts (title, content, image_url, category, user_id) VALUES (?, ?, ?, ?, ?)',
            (title, content, image_url, category, user_id)
        )
        post_id = cursor.lastrowid

        if category == 'Опитування' and poll_options:
            for option_text in poll_options:
                if option_text.strip():
                    cursor.execute('INSERT INTO poll_options (option_text, post_id) VALUES (?, ?)', (option_text.strip(), post_id))

        conn.commit()
        conn.close()

        if socketio:
            conn = sqlite3.connect('messenger.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                'SELECT p.id, p.title, p.content, p.image_url, p.category, p.created_at, u.first_name, u.last_name FROM posts p JOIN users u ON p.user_id = u.id WHERE p.id = ?',
                (post_id,)
            )
            post = cursor.fetchone()
            conn.close()

            if post:
                post_data = dict(post)
                post_data['like_count'] = 0
                socketio.emit('new_post', post_data)

        return json.dumps({'status': 'success', 'message': 'Post created successfully'}), 200

    except Exception as e:
        return json.dumps({'status': 'error', 'message': f'Помилка створення поста: {str(e)}'}), 500