from flask import Blueprint, jsonify, request
from src.DTO.UserDTO import *
from src.DATA.UserToDatabase import *
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

    password = request.form.get('password')
    byte_pwd = password.encode('utf-8')
    pwd_hash = bcrypt.hashpw(byte_pwd, bcrypt.gensalt())  # hashed pwd
    age = request.form.get('age')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    user = UserDTO(generate_id(), firstname, lastname, age, email, pwd_hash)
    create_user(user)