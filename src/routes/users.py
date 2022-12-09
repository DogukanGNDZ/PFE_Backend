from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.UserDTO import *
from src.data.UserToDatabase import *
import uuid
import bcrypt
import jwt
import datetime

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
    age = 0
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    user = UserDTO(generate_id(), firstname, lastname, age,
                   email, pwd_hash, 0, 0, "", 0, "", "")
    return create_user(user)


def generate_jwt(user_id):
    # Create the payload with the user's ID and an expiration date
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    # Sign the JWT using a secret key
    # do not forget to put this key in the env filee
    jwt_token = jwt.encode(payload, 'MBJDT_Corporation')

    return jwt_token


@users_bp.route("/login", methods=["POST"])
@cross_origin()
def login():
    password = request.json.get('password')
    byte_pwd = password.encode('UTF-8')
    email = request.json.get('email')
    if check_user(byte_pwd, email):
        get_user = fetch_user_email(email)
        print(get_user[id])
        return generate_jwt(get_user[id])

    else:
        response = make_response("Wrong password", 400)
        return response

