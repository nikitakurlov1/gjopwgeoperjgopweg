import json
from flask import session

def logout_user(request):
    try:
        # Clear the session
        session.clear()
        
        return json.dumps({
            'status': 'redirect',
            'url': '/index.html'
        }), 200
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Помилка виходу: {str(e)}'
        }), 500