from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.UserDTO import *
from src.data.UserToDatabase import *
import uuid
import bcrypt

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("", methods=["GET"])
def get_all_users():
    id = request.args.get("id", default=1, type=int)
    if (id == 1):
        return fetch_all_users()
    return fetch_user(id)


# generate a new id
def generate_id():
    return str(uuid.uuid4())


@users_bp.route("/register", methods=["POST"])
@cross_origin()
def register():
    # Get the values from the request

    password = request.json.get('password')
    byte_pwd = password.encode('UTF-8')
    pwd_hash = bcrypt.hashpw(byte_pwd, bcrypt.gensalt())  # hashed pwd
    age = request.json.get('age')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    user = UserDTO(generate_id(), firstname, lastname, age, email, pwd_hash)
    return create_user(user)


@users_bp.route("/login", methods=["POST"])
@cross_origin()
def login():
    password = request.json.get('password')
    byte_pwd = password.encode('UTF-8')
    email = request.json.get('email')
    if check_user(email, byte_pwd):
        response = make_response(200)
        return response
    else:
        response = make_response("Wrong password", 400)
        return response
