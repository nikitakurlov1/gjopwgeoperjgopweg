import requests
import json

# Test that registration creates proper session
def test_registration_session():
    # Create a session object to persist cookies
    session = requests.Session()
    
    url = "http://localhost:5001/api/register"
    payload = {
        "first_name": "Тест",
        "last_name": "Сесія",
        "class": "11-А",
        "category": "Учень",
        "school": "Тестовий ліцей",
        "phone": "+380 (99) 999-99-99",
        "password": "testpassword123"
    }
    headers = {'Content-Type': 'application/json'}
    
    response = session.post(url, data=json.dumps(payload), headers=headers)
    print("Registration Response:", response.text)
    print("Registration Status Code:", response.status_code)
    
    # Now try to access a protected endpoint that requires a session
    profile_url = "http://localhost:5001/api/profile"
    profile_response = session.get(profile_url)
    print("Profile Access Response:", profile_response.text)
    print("Profile Access Status Code:", profile_response.status_code)
    
    return response.status_code, profile_response.status_code

if __name__ == "__main__":
    print("Testing Registration Session Creation...")
    reg_status, profile_status = test_registration_session()
    if reg_status == 200 and profile_status == 200:
        print("SUCCESS: Registration properly creates session and user can access protected endpoints!")
    else:
        print("FAILURE: Session not properly created or accessible")