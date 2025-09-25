# School Messenger Authentication System

This is a complete authentication system for a school messenger application with login, registration, post functionality, likes, and comments.

## Features

- Mobile-first responsive design
- Light theme with specific color scheme
- User registration with validation
- User login with authentication
- Post creation and viewing
- Like functionality for posts
- Comment functionality for posts
- SQLite database backend
- Separate API endpoints for each action

## Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite

## Project Structure

```
.
├── README.md           # This file
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── messenger.db        # SQLite database (created automatically)
├── static/             # Frontend files
│   ├── index.html      # Login page
│   ├── register.html   # Registration page
│   ├── lenta.html      # Main feed page
│   ├── create_post.html # Post creation page
│   ├── styles.css      # Styling for all pages
│   └── script.js       # Client-side functionality
└── api/
    ├── register.py     # Registration endpoint
    ├── login.py        # Login endpoint
    ├── logout.py       # Logout endpoint
    ├── posts.py        # Posts retrieval endpoint
    ├── create_post.py  # Post creation endpoint
    ├── like_post.py    # Post like endpoint
    └── comments.py     # Comments endpoints
```

## Setup Instructions

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and navigate to `http://localhost:5000`

## Design Specifications

- Theme: Light
- Background color: #FFFFFF
- Text color: #333333
- Button color: #90EE90 (hover: #7CFC00)
- Font family: Roboto, sans-serif
- Layout: Mobile-first, adaptive single-column layout

## API Endpoints

- POST `/api/register` - User registration
- POST `/api/login` - User login
- POST `/api/logout` - User logout
- GET `/api/posts` - Retrieve all posts
- POST `/api/create_post` - Create a new post
- POST `/api/posts/<post_id>/like` - Like/unlike a post
- GET `/api/posts/<post_id>/comments` - Retrieve comments for a post
- POST `/api/posts/<post_id>/comments` - Add a comment to a post

API endpoints return JSON responses with either:
- Success: `{"status": "redirect", "url": "/lenta.html"}` or `{"status": "success", "data": "[data]"}`
- Error: `{"status": "error", "message": "Error description"}`

## Manual Testing

1. Open your browser and go to `http://localhost:5000`
2. You'll be redirected to the login page
3. Click "Немає акаунту? Зареєструватися" to go to the registration page
4. Fill out the registration form and submit
5. After successful registration, you'll be redirected to the feed page
6. Click "Створити" in the bottom navigation to create a new post
7. Fill out the post form and submit
8. You'll be redirected back to the feed page where you can see your post
9. Click the "Like" button to like a post
10. Click the "Comment" button to open the comments section and add a comment

## Database Structure

The SQLite database contains the following tables:

1. `users` table with columns:
   - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - first_name (TEXT, NOT NULL)
   - last_name (TEXT, NOT NULL)
   - class (TEXT)
   - category (TEXT, NOT NULL)
   - school (TEXT, NOT NULL)
   - phone (TEXT, NOT NULL, UNIQUE)
   - password_hash (TEXT, NOT NULL)

2. `posts` table with columns:
   - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - title (TEXT, NOT NULL)
   - content (TEXT, NOT NULL)
   - image_url (TEXT)
   - category (TEXT, NOT NULL)
   - created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
   - user_id (INTEGER, NOT NULL, FOREIGN KEY REFERENCES users(id))

3. `likes` table with columns:
   - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - user_id (INTEGER, NOT NULL, FOREIGN KEY REFERENCES users(id))
   - post_id (INTEGER, NOT NULL, FOREIGN KEY REFERENCES posts(id))
   - UNIQUE constraint on (user_id, post_id)

4. `comments` table with columns:
   - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - content (TEXT, NOT NULL)
   - created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
   - user_id (INTEGER, NOT NULL, FOREIGN KEY REFERENCES users(id))
   - post_id (INTEGER, NOT NULL, FOREIGN KEY REFERENCES posts(id))