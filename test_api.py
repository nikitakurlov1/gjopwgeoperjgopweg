import requests
import json

# Test registration
def test_registration():
    url = "http://localhost:5001/api/register"
    payload = {
        "first_name": "Тест",
        "last_name": "Користувач",
        "class": "10-Б",
        "category": "Учень",
        "school": "Первозванівський ліцей",
        "phone": "+380 (50) 123-45-67",
        "password": "testpassword"
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print("Registration Response:", response.text)
    return response.status_code

# Test login
def test_login():
    url = "http://localhost:5001/api/login"
    payload = {
        "phone": "+380 (38) 099-16-94",
        "password": "12345678"
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print("Login Response:", response.text)
    return response.status_code

if __name__ == "__main__":
    print("Testing Registration API...")
    reg_status = test_registration()
    print(f"Registration Status Code: {reg_status}\n")
    
    print("Testing Login API...")
    login_status = test_login()
    print(f"Login Status Code: {login_status}")