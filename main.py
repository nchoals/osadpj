from routes import app, socketio
from models import db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # app.run(debug=True)
    socketio.run(app, debug=True, port=8080, allow_unsafe_werkzeug=True)
