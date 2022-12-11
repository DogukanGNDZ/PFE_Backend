from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.UserDTO import *
from src.data.UserToDatabase import *
from src.routes.auth import authorize
import uuid
import bcrypt
import ast

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
    if(check_mail(email)):
        return make_response("Email already use", 400)   
    else:           
        return create_user(user)



@users_bp.route("/myprofil", methods=["GET"])
@cross_origin()
def get_my_profil():
    token = request.headers.get('Authorize')
    claims = authorize(token)
    if claims.status_code==498 or claims.status_code==401:
        return make_response('Invalid Token',498)
    return fetch_user(ast.literal_eval(claims.data.decode('utf-8'))["user_id"])
    