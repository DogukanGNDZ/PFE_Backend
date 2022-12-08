from flask import Blueprint

connect_bp = Blueprint("test", __name__, url_prefix="/test")


@connect_bp.route("", methods=["GET"])
def login_user():
    word = 'there'
    return 'this is the way is: {}'.format(word)
