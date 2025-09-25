import requests
import json

def test_likes_comments_attribution():
    # Create a session object to persist cookies
    session = requests.Session()
    
    # First, register a new user
    register_url = "http://localhost:5001/api/register"
    register_payload = {
        "first_name": "Тест",
        "last_name": "ЛайкиКоментарі",
        "class": "11-Б",
        "category": "Учень",
        "school": "Тестовий ліцей",
        "phone": "+380 (88) 888-88-88",
        "password": "testpassword123"
    }
    register_headers = {'Content-Type': 'application/json'}
    
    register_response = session.post(register_url, data=json.dumps(register_payload), headers=register_headers)
    print("Registration Response:", register_response.text)
    print("Registration Status Code:", register_response.status_code)
    
    if register_response.status_code != 200:
        print("FAILED: Registration failed")
        return
    
    # Create a post
    create_post_url = "http://localhost:5001/api/create_post"
    post_payload = {
        "title": "Тестовий пост для перевірки лайків",
        "content": "Це тестовий пост для перевірки правильного створення лайків та коментарів",
        "category": "Новини"
    }
    
    post_response = session.post(create_post_url, data=json.dumps(post_payload), headers=register_headers)
    print("Create Post Response:", post_response.text)
    print("Create Post Status Code:", post_response.status_code)
    
    if post_response.status_code != 200:
        print("FAILED: Post creation failed")
        return
    
    # Get posts to find the post ID
    posts_url = "http://localhost:5001/api/posts"
    posts_response = session.get(posts_url)
    posts_data = json.loads(posts_response.text)
    
    if posts_data['status'] != 'success':
        print("FAILED: Could not retrieve posts")
        return
    
    # Find our test post
    test_post = None
    for post in posts_data['data']:
        if post['title'] == "Тестовий пост для перевірки лайків":
            test_post = post
            break
    
    if not test_post:
        print("FAILED: Could not find test post")
        return
    
    post_id = test_post['id']
    print(f"Found test post with ID: {post_id}")
    
    # Like the post
    like_url = f"http://localhost:5001/api/posts/{post_id}/like"
    like_response = session.post(like_url)
    print("Like Response:", like_response.text)
    print("Like Status Code:", like_response.status_code)
    
    if like_response.status_code != 200:
        print("FAILED: Liking post failed")
        return
    
    # Add a comment
    comment_url = f"http://localhost:5001/api/posts/{post_id}/comments"
    comment_payload = {
        "content": "Тестовий коментар для перевірки правильного створення"
    }
    
    comment_response = session.post(comment_url, data=json.dumps(comment_payload), headers=register_headers)
    print("Comment Response:", comment_response.text)
    print("Comment Status Code:", comment_response.status_code)
    
    if comment_response.status_code != 200:
        print("FAILED: Commenting failed")
        return
    
    # Verify the comment was attributed correctly
    comments_response = session.get(comment_url)
    comments_data = json.loads(comments_response.text)
    
    if comments_data['status'] != 'success':
        print("FAILED: Could not retrieve comments")
        return
    
    if len(comments_data['data']) == 0:
        print("FAILED: No comments found")
        return
    
    comment = comments_data['data'][0]
    if comment['author_first_name'] == "Тест" and comment['author_last_name'] == "ЛайкиКоментарі":
        print("SUCCESS: Comment correctly attributed to the logged-in user!")
    else:
        print(f"FAILED: Comment attributed to {comment['author_first_name']} {comment['author_last_name']} instead of the logged-in user")
        return
    
    print("All tests passed! Likes and comments are correctly attributed to the logged-in user.")

if __name__ == "__main__":
    print("Testing Likes and Comments Attribution...")
    test_likes_comments_attribution()