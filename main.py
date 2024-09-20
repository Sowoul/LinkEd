from flask import Flask
from flask_migrate import Migrate

from socket_handler import socket

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "IDK123"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    from models import User, db, Post
    db.init_app(app)
    socket.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        print("imported user")
        db.create_all()
    from routes import main_routes
    app.register_blueprint(main_routes)
    return app

if __name__ == '__main__':
    app = create_app()
    socket.run(app=app,port=8080, debug=True)
