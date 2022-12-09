from flask import Flask

from src.routes.users import users_bp
from src.routes.clubs import clubs_bp
from src.routes.coachs import coachs_bp
from src.routes.sports import sports_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    app.register_blueprint(clubs_bp)
    app.register_blueprint(coachs_bp)
    app.register_blueprint(sports_bp)
    return app
