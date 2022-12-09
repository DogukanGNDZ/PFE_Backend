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
    age = 0
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    user = UserDTO(generate_id(), firstname, lastname, age,
                   email, pwd_hash, 0, 0, "", 0, "", "")
    return create_user(user)


@users_bp.route("/login", methods=["POST"])
@cross_origin()
def login():
    password = request.json.get('password')
    byte_pwd = password.encode('UTF-8')
    email = request.json.get('email')
    if check_user(byte_pwd, email):
        print("work")
        return "login successful"
    else:
        response = make_response("Wrong password", 400)
        return response


@users_bp.route("/update", methods=["PUT"])
@cross_origin()
def update_data_user():
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    age = request.json.get('age')
    size = request.json.get('size')
    weight = request.json.get('weight')
    post = request.json.get('post')
    nYE = request.json.get('number_year_experience')
    description = request.json.get('description')
    picture = request.json.get('picture')
    print("avant create user dto")
    user = UserDTO(0, firstname, lastname, age, email, "", size,
                   weight, post, nYE, description, picture)
    return update_user(user)
