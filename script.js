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