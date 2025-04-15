"""Create an application instance."""
from server.app import app
from server.extensions import socketio

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
