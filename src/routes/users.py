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
    print("aaaaaaaaaaaaaaaaaaaaaa")
    password = request.json.get('password')
    if (password is not None):
        print("y a pas rien")
    else:
        print("y a rien")
    print(password)
    byte_pwd = password.encode('UTF-8')
    pwd_hash = bcrypt.hashpw(byte_pwd, bcrypt.gensalt())  # hashed pwd
    age = 0
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    user = UserDTO(generate_id(), firstname, lastname, age,
                   email, pwd_hash, 0, 0, "", 0, "", "")
    if(check_mail(email)):
        return make_response("Email already use", 400)   
    else:           
        return create_user(user)


