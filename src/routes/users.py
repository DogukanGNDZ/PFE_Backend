from flask import Blueprint, jsonify, request
from src.dto.UserDTO import *
from src.data.UserToDatabase import *
import uuid
import bcrypt

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("", methods=["GET"])
def get_all_users():
    all_users = [{"id": 1, "name": "bob"}, {"id": 1, "name": "Joe"}]
    return jsonify(all_users)


# generate a new id
def generate_id():
    return str(uuid.uuid4())


@users_bp.route("/register", methods=["POST"])
def register():
    # Get the values from the request
    print("aaaaaaaaaaaaaaaaaaaaaa")
    password = request.json.get('password')
    if (password is not None):
        print("y a pas rien")
    else:
        print("y a rien")
    print(password)
    byte_pwd = password.encode('UTF-8')
    pwd_hash = bcrypt.hashpw(byte_pwd, bcrypt.gensalt())  # hashed pwd
    age = request.json.get('age')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    user = UserDTO(generate_id(), firstname, lastname, age, email, pwd_hash)
    return create_user(user)