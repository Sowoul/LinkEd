from flask import Flask
from flask_migrate import Migrate

from socket_handler import socket

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "IDK123"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    from models import Post, User, db
    db.init_app(app)
    socket.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    from blueprints.comments import comms
    from blueprints.connections import connections
    from blueprints.likes import likes
    from blueprints.posts import posts
    from blueprints.publications import publications
    from blueprints.routes import main_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(comms)
    app.register_blueprint(likes)
    app.register_blueprint(connections)
    app.register_blueprint(posts)
    app.register_blueprint(publications)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8080, debug=True)
