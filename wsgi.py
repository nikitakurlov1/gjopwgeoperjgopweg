import os
from app import app, socketio

# Get the port from the environment variable, default to 5000 if not set
port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    # Run without debug mode and with allow_unsafe_werkzeug for production
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)