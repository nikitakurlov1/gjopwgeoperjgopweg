// Initialize global WebSocket connection
const socket = io();

// Handle login form submission
document.getElementById('loginForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;
    
    // Simple validation
    if (!phone || !password) {
        alert('Будь ласка, заповніть всі поля');
        return;
    }
    
    // Prepare data for API call
    const formData = {
        phone: phone,
        password: password
    };
    
    // Send login request
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'redirect') {
            window.location.href = data.url;
        } else {
            alert(data.message || 'Помилка входу');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Сталася помилка. Спробуйте ще раз.');
    });
});

// Handle registration form submission
document.getElementById('registerForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const userClass = document.getElementById('class').value;
    const category = document.getElementById('category').value;
    const school = document.getElementById('school').value;
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;
    
    // Simple validation
    if (!firstName || !lastName || !category || !school || !phone || !password) {
        alert('Будь ласка, заповніть всі обов\'язкові поля');
        return;
    }
    
    // Validate password length
    if (password.length < 8) {
        alert('Пароль має містити мінімум 8 символів');
        return;
    }
    
    // Prepare data for API call
    const formData = {
        first_name: firstName,
        last_name: lastName,
        class: userClass,
        category: category,
        school: school,
        phone: phone,
        password: password
    };
    
    // Send registration request
    fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'redirect') {
            window.location.href = data.url;
        } else {
            alert(data.message || 'Помилка реєстрації');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Сталася помилка. Спробуйте ще раз.');
    });
});

// Load posts for lenta.html
if (document.getElementById('postFeed')) {
    loadPosts();
    
    // Add logout functionality
    document.getElementById('logoutButton')?.addEventListener('click', function() {
        fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'redirect') {
                window.location.href = data.url;
            } else {
                alert(data.message || 'Помилка виходу');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Сталася помилка. Спробуйте ще раз.');
        });
    });
    
    // Add search functionality
    document.getElementById('searchInput')?.addEventListener('input', function() {
        loadPosts();
    });
    
    // Add category filter functionality
    document.getElementById('categoryFilter')?.addEventListener('change', function() {
        loadPosts();
    });
}

/**
 * Load posts from the API
 * @returns {void}
 */
function loadPosts() {
    fetch('/api/posts')
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            displayPosts(data.data);
        } else {
            console.error('Error loading posts:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayPosts([]); // Display empty state on error
    });
}

/**
 * Display posts in the feed
 * @param {Array} posts - Array of post objects
 * @returns {void}
 */
function displayPosts(posts) {
    const postFeed = document.getElementById('postFeed');
    if (!postFeed) return;
    
    postFeed.innerHTML = '';
    
    if (posts.length === 0) {
        postFeed.innerHTML = '<p class="no-posts">Поки немає постів. Будьте першим, хто створить пост!</p>';
        return;
    }
    
    posts.forEach(post => {
        // Generate poll options HTML if this is a poll post
        let pollOptionsHtml = '';
        if (post.category === 'Опитування' && post.poll_options && post.poll_options.length > 0) {
            pollOptionsHtml = '<div class="poll-options"><h4>Варіанти відповідей:</h4><ul>';
            let totalVotes = 0;
            
            // Calculate total votes for percentage calculation
            post.poll_options.forEach(option => {
                totalVotes += option.vote_count;
            });
            
            post.poll_options.forEach(option => {
                const percentage = totalVotes > 0 ? Math.round((option.vote_count / totalVotes) * 100) : 0;
                const userVotedClass = option.user_voted ? 'user-voted' : '';
                
                pollOptionsHtml += `
                    <li class="poll-option ${userVotedClass}" data-option-id="${option.id}" data-post-id="${post.id}">
                        <div class="option-content">
                            <span class="option-text">${option.option_text}</span>
                            <span class="vote-count">(${option.vote_count} голосів)</span>
                        </div>
                        <div class="vote-bar">
                            <div class="vote-bar-fill" style="width: ${percentage}%"></div>
                        </div>
                        <div class="vote-percentage">${percentage}%</div>
                    </li>
                `;
            });
            
            pollOptionsHtml += '</ul>';
            
            if (!post.user_voted) {
                pollOptionsHtml += '<button class="submit-vote-btn" data-post-id="' + post.id + '">Проголосувати</button>';
            } else {
                pollOptionsHtml += '<p class="vote-status">Ви вже проголосували</p>';
            }
            
            pollOptionsHtml += '</div>';
        }
        
        const postElement = document.createElement('div');
        postElement.className = 'post-card';
        postElement.innerHTML = `
            <div class="post-header">
                <div class="author-info">
                    <div class="author-avatar">👤</div>
                    <div class="author-details">
                        <div class="author-name">${post.author_first_name} ${post.author_last_name}</div>
                        <div class="post-timestamp">${formatDate(post.created_at)}</div>
                    </div>
                </div>
                <div class="category-badge ${post.category.toLowerCase()}">${post.category}</div>
            </div>
            <div class="post-content">
                <h3 class="post-title">${post.title}</h3>
                <p class="post-text">${post.content}</p>
                ${pollOptionsHtml}
                ${post.image_url ? `<img src="${post.image_url}" alt="Post image" class="post-image">` : ''}
            </div>
            <div class="post-actions">
                <button class="action-button like-button" data-post-id="${post.id}">
                    <span class="action-icon">👍</span>
                    <span class="action-text">Подобається</span>
                    <span class="action-count">${post.like_count}</span>
                </button>
                <button class="action-button comment-button" data-post-id="${post.id}">
                    <span class="action-icon">💬</span>
                    <span class="action-text">Коментувати</span>
                </button>
            </div>
            <div class="comments-section" id="comments-${post.id}" style="display: none;">
                <div class="comments-list" id="comments-list-${post.id}">
                    <!-- Comments will be loaded here -->
                </div>
                <form class="comment-form" data-post-id="${post.id}">
                    <input type="text" class="comment-input" placeholder="Напишіть коментар..." required>
                    <button type="submit" class="submit-comment-btn">Відправити</button>
                </form>
            </div>
        `;
        postFeed.appendChild(postElement);
    });
    
    // Add event listeners for poll options
    document.querySelectorAll('.poll-option').forEach(option => {
        option.addEventListener('click', function() {
            // Only allow selection if user hasn't voted yet
            const postId = this.getAttribute('data-post-id');
            const postElement = posts.find(p => p.id == postId);
            
            if (postElement && !postElement.user_voted) {
                // Remove selection from other options in the same poll
                const siblings = this.parentNode.querySelectorAll('.poll-option');
                siblings.forEach(sibling => {
                    sibling.classList.remove('selected');
                });
                
                // Add selection to clicked option
                this.classList.add('selected');
            }
        });
    });
    
    // Add event listeners for vote buttons
    document.querySelectorAll('.submit-vote-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const selectedOption = document.querySelector(`.poll-option.selected[data-post-id="${postId}"]`);
            
            if (!selectedOption) {
                alert('Будь ласка, виберіть варіант відповіді');
                return;
            }
            
            const optionId = selectedOption.getAttribute('data-option-id');
            
            // Send vote to server
            fetch(`/api/posts/${postId}/vote`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ option_id: optionId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Reload posts to show updated vote counts
                    loadPosts();
                } else {
                    alert(data.message || 'Помилка голосування');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Сталася помилка. Спробуйте ще раз.');
            });
        });
    });
    
    // Remove existing event listeners to prevent duplication
    document.querySelectorAll('.like-button').forEach(button => {
        // Create a new button element to remove all event listeners
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
        
        // Add event listener to the new button
        newButton.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            toggleLike(postId);
        });
    });
    
    // Remove existing event listeners to prevent duplication
    document.querySelectorAll('.comment-button').forEach(button => {
        // Create a new button element to remove all event listeners
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
        
        // Add event listener to the new button
        newButton.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            toggleComments(postId);
        });
    });
    
    // Remove existing event listeners to prevent duplication
    document.querySelectorAll('.comment-form').forEach(form => {
        // Create a new form element to remove all event listeners
        const newForm = form.cloneNode(true);
        form.parentNode.replaceChild(newForm, form);
        
        // Add event listener to the new form
        newForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.getAttribute('data-post-id');
            const commentInput = this.querySelector('.comment-input');
            const commentText = commentInput.value.trim();
            if (commentText) {
                postComment(postId, commentText);
                commentInput.value = '';
            }
        });
    });
}

/**
 * Format date for display
 * @param {string} dateString - Date string to format
 * @returns {string} Formatted date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('uk-UA') + ' ' + date.toLocaleTimeString('uk-UA', {hour: '2-digit', minute:'2-digit'});
}

// Handle create post form submission
document.getElementById('createPostForm')?.addEventListener('submit', function(e) {
    // Step 1: Ensure event.preventDefault() is the very first line
    e.preventDefault();
    
    // Step 2: Disable the submit button to prevent double clicks
    const submitButton = document.querySelector('#createPostForm button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = 'Публікація...'; // Optional: show feedback to user
    }
    
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const category = document.getElementById('category').value;
    
    // Prepare data for API call
    const formData = {
        title: title,
        content: content,
        category: category
    };
    
    // If category is "Опитування", collect poll options
    if (category === 'Опитування') {
        const pollOptions = [];
        const pollOptionInputs = document.querySelectorAll('input[name="poll_options[]"]');
        
        // Check if at least one poll option is filled
        let hasFilledOption = false;
        pollOptionInputs.forEach(input => {
            if (input.value.trim() !== '') {
                pollOptions.push(input.value.trim());
                hasFilledOption = true;
            }
        });
        
        // Validate that at least one poll option is provided
        if (!hasFilledOption) {
            alert('Будь ласка, додайте хоча б один варіант відповіді для опитування');
            // Re-enable the button
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Опублікувати'; // Restore original text
            }
            return;
        }
        
        // Add poll options to form data
        formData.poll_options = pollOptions;
    }
    
    // Send create post request
    fetch('/api/create_post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'redirect') {
            // Instead of immediately redirecting, first refresh the posts feed
            // Then redirect to the feed page
            window.location.href = data.url;
        } else {
            // Step 3: Re-enable the button on failure
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Опублікувати'; // Restore original text
            }
            alert(data.message || 'Помилка створення поста');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Step 3: Re-enable the button on failure
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = 'Опублікувати'; // Restore original text
        }
        alert('Сталася помилка. Спробуйте ще раз.');
    });
});

// Add event listener for category selection to show/hide poll options
document.getElementById('category')?.addEventListener('change', function() {
    const category = this.value;
    const pollOptionsContainer = document.getElementById('pollOptionsContainer');
    
    if (category === 'Опитування') {
        pollOptionsContainer.style.display = 'block';
    } else {
        pollOptionsContainer.style.display = 'none';
    }
});

// Add event listener for adding new poll options
document.getElementById('addPollOptionBtn')?.addEventListener('click', function() {
    const pollOptionsContainer = document.getElementById('pollOptionsContainer');
    const newOptionDiv = document.createElement('div');
    newOptionDiv.className = 'form-group';
    newOptionDiv.innerHTML = '<input type="text" name="poll_options[]" placeholder="Новий варіант">';
    pollOptionsContainer.insertBefore(newOptionDiv, this);
});

/**
 * Toggle like for a post
 * @param {number} postId - ID of the post to like/unlike
 * @returns {void}
 */
function toggleLike(postId) {
    fetch(`/api/posts/${postId}/like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update the like button UI
            const likeButton = document.querySelector(`.like-button[data-post-id="${postId}"]`);
            const likeCount = likeButton.querySelector('.action-count');
            
            likeCount.textContent = data.data.new_like_count;
            
            // Change button appearance based on like status
            if (data.data.liked_by_user) {
                likeButton.classList.add('liked');
            } else {
                likeButton.classList.remove('liked');
            }
        } else {
            alert(data.message || 'Помилка при зміні статусу вподобання');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Сталася помилка. Спробуйте ще раз.');
    });
}

/**
 * Toggle comments section for a post
 * @param {number} postId - ID of the post to toggle comments for
 * @returns {void}
 */
function toggleComments(postId) {
    const commentsSection = document.getElementById(`comments-${postId}`);
    if (commentsSection.style.display === 'none') {
        commentsSection.style.display = 'block';
        // Load comments when section is opened
        fetchComments(postId);
    } else {
        commentsSection.style.display = 'none';
    }
}

/**
 * Fetch comments for a post
 * @param {number} postId - ID of the post to fetch comments for
 * @returns {void}
 */
function fetchComments(postId) {
    fetch(`/api/posts/${postId}/comments`)
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            displayComments(postId, data.data);
        } else {
            console.error('Error fetching comments:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

/**
 * Display comments for a post
 * @param {number} postId - ID of the post
 * @param {Array} comments - Array of comment objects
 * @returns {void}
 */
function displayComments(postId, comments) {
    const commentsList = document.getElementById(`comments-list-${postId}`);
    commentsList.innerHTML = '';
    
    if (comments.length === 0) {
        commentsList.innerHTML = '<p class="no-comments">Поки немає коментарів. Будьте першим, хто залишить коментар!</p>';
        return;
    }
    
    comments.forEach(comment => {
        const commentElement = document.createElement('div');
        commentElement.className = 'comment';
        commentElement.innerHTML = `
            <div class="comment-author">${comment.author_first_name} ${comment.author_last_name}</div>
            <div class="comment-content">${comment.content}</div>
            <div class="comment-timestamp">${formatDate(comment.created_at)}</div>
        `;
        commentsList.appendChild(commentElement);
    });
}

/**
 * Post a new comment
 * @param {number} postId - ID of the post to comment on
 * @param {string} commentText - Text of the comment
 * @returns {void}
 */
function postComment(postId, commentText) {
    fetch(`/api/posts/${postId}/comments`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: commentText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Add the new comment to the list
            const commentsList = document.getElementById(`comments-list-${postId}`);
            // Remove "no comments" message if it exists
            const noCommentsMsg = commentsList.querySelector('.no-comments');
            if (noCommentsMsg) {
                noCommentsMsg.remove();
            }
            
            const commentElement = document.createElement('div');
            commentElement.className = 'comment';
            commentElement.innerHTML = `
                <div class="comment-author">${data.data.author_first_name} ${data.data.author_last_name}</div>
                <div class="comment-content">${data.data.content}</div>
                <div class="comment-timestamp">${formatDate(data.data.created_at)}</div>
            `;
            commentsList.appendChild(commentElement);
        } else {
            alert(data.message || 'Помилка при додаванні коментаря');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Сталася помилка. Спробуйте ще раз.');
    });
}

// WebSocket event handlers for real-time updates

// Handle new post event
socket.on('new_post', function(post_data) {
    // Check if we're on the lenta.html page (feed page)
    if (document.getElementById('postFeed')) {
        // Create a new post element
        let pollOptionsHtml = '';
        if (post_data.category === 'Опитування') {
            pollOptionsHtml = '<div class="poll-options"><h4>Варіанти відповідей:</h4><ul>';
            pollOptionsHtml += '</ul>';
            pollOptionsHtml += '<p class="vote-status">Ви ще не голосували</p>';
            pollOptionsHtml += '</div>';
        }
        
        const postElement = document.createElement('div');
        postElement.className = 'post-card';
        postElement.innerHTML = `
            <div class="post-header">
                <div class="author-info">
                    <div class="author-avatar">👤</div>
                    <div class="author-details">
                        <div class="author-name">${post_data.author_first_name} ${post_data.author_last_name}</div>
                        <div class="post-timestamp">${formatDate(post_data.created_at)}</div>
                    </div>
                </div>
                <div class="category-badge ${post_data.category.toLowerCase()}">${post_data.category}</div>
            </div>
            <div class="post-content">
                <h3 class="post-title">${post_data.title}</h3>
                <p class="post-text">${post_data.content}</p>
                ${pollOptionsHtml}
                ${post_data.image_url ? `<img src="${post_data.image_url}" alt="Post image" class="post-image">` : ''}
            </div>
            <div class="post-actions">
                <button class="action-button like-button" data-post-id="${post_data.id}">
                    <span class="action-icon">👍</span>
                    <span class="action-text">Подобається</span>
                    <span class="action-count">${post_data.like_count}</span>
                </button>
                <button class="action-button comment-button" data-post-id="${post_data.id}">
                    <span class="action-icon">💬</span>
                    <span class="action-text">Коментувати</span>
                </button>
            </div>
            <div class="comments-section" id="comments-${post_data.id}" style="display: none;">
                <div class="comments-list" id="comments-list-${post_data.id}">
                    <!-- Comments will be loaded here -->
                </div>
                <form class="comment-form" data-post-id="${post_data.id}">
                    <input type="text" class="comment-input" placeholder="Напишіть коментар..." required>
                    <button type="submit" class="submit-comment-btn">Відправити</button>
                </form>
            </div>
        `;
        
        // Prepend the new post to the top of the feed
        const postFeed = document.getElementById('postFeed');
        postFeed.insertBefore(postElement, postFeed.firstChild);
        
        // Add event listeners for the new post
        const likeButton = postElement.querySelector('.like-button');
        likeButton.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            toggleLike(postId);
        });
        
        const commentButton = postElement.querySelector('.comment-button');
        commentButton.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            toggleComments(postId);
        });
        
        const commentForm = postElement.querySelector('.comment-form');
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.getAttribute('data-post-id');
            const commentInput = this.querySelector('.comment-input');
            const commentText = commentInput.value.trim();
            if (commentText) {
                postComment(postId, commentText);
                commentInput.value = '';
            }
        });
    }
});

// Handle new comment event
socket.on('new_comment', function(comment_data) {
    // Find the post on the current page with the matching post_id
    const commentsList = document.getElementById(`comments-list-${comment_data.post_id}`);
    if (commentsList) {
        // Remove "no comments" message if it exists
        const noCommentsMsg = commentsList.querySelector('.no-comments');
        if (noCommentsMsg) {
            noCommentsMsg.remove();
        }
        
        // Create and append the new comment
        const commentElement = document.createElement('div');
        commentElement.className = 'comment';
        commentElement.innerHTML = `
            <div class="comment-author">${comment_data.author_first_name} ${comment_data.author_last_name}</div>
            <div class="comment-content">${comment_data.content}</div>
            <div class="comment-timestamp">${formatDate(comment_data.created_at)}</div>
        `;
        commentsList.appendChild(commentElement);
        
        // Scroll to the new comment
        commentElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});

// Handle post update event (like count changes)
socket.on('post_update', function(update_data) {
    // Find the post with the matching post_id and update the like counter
    const likeCountElement = document.querySelector(`.like-button[data-post-id="${update_data.post_id}"] .action-count`);
    if (likeCountElement) {
        likeCountElement.textContent = update_data.new_like_count;
    }
});

// Handle private message event
socket.on('private_message', function(message_data) {
    // Check if we're on the trust_box.html page
    if (window.location.pathname.includes('trust_box.html')) {
        // Display the new message in the chat window
        const chatWindow = document.getElementById('trustBoxChat');
        if (chatWindow) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${message_data.sent_by_admin ? 'admin-message' : 'student-message'}`;
            
            const senderName = message_data.sent_by_admin ? 'Адміністратор' : message_data.first_name + ' ' + message_data.last_name;
            
            messageDiv.innerHTML = `
                <div class="message-sender">${senderName}</div>
                <div class="message-text">${message_data.message_text}</div>
                <div class="message-time">${formatDate(message_data.timestamp)}</div>
            `;
            
            chatWindow.appendChild(messageDiv);
            
            // Scroll to bottom
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    } else {
        // Show a notification indicator on the 'Чати' icon in the header
        // This would require implementing a notification system
        console.log('New private message received:', message_data);
    }
});
