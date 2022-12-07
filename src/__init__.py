from flask import Flask

from src.routes.connect import connect_bp
from src.routes.users import users_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(connect_bp)
    app.register_blueprint(users_bp)
    return app
