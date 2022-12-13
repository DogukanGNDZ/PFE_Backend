from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.UserDTO import *
from src.data.UserToDatabase import *
from src.data.AdressToDatabase import fetch_user_adress
from src.routes.auth import authorize, get_role
import uuid
import bcrypt
import ast

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("", methods=["GET"])
@cross_origin()
def get_all_users():
    id = request.args.get("id", default="", type=str)
    if (id == ""):
        return fetch_all_users()
    return fetch_user(id)


@users_bp.route("/id/<id>", methods=["GET"])
@cross_origin()
def get_user_id(id):
    user = fetch_user(id)
    if (user is not None):
        return make_response(user, 200)
    return make_response("User not found", 404)


@users_bp.route("/email/<email>", methods=["GET"])
@cross_origin()
def get_user_email(email):
    user = fetch_user_email(email)
    if (user is not None):
        return make_response(user, 200)
    return make_response("User not found", 404)


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
    role = request.json.get('role')
    user = UserDTO(generate_id(), firstname, lastname, age,
                   email, pwd_hash, 0, 0, "", 0, "", "")
    if (check_mail(email)):
        return make_response("Email already use", 400)
    else:
        create_user(user)
        return make_response("created", 200)


@users_bp.route("/myprofil", methods=["GET"])
@cross_origin()
def get_my_profil():
    token = request.headers.get('Authorize')
    claims = authorize(token)
    if claims.status_code == 498 or claims.status_code == 401:
        return make_response('Invalid Token', 498)
    user = fetch_user(ast.literal_eval(claims.data.decode('utf-8'))["user_id"])

    if (user is not None):
        return make_response(user, 200)
    return make_response("User id not found", 404)


@users_bp.route("/update", methods=["PUT"])
@cross_origin()
def update_data_user():
    token = request.headers.get('Authorize')
    claims = authorize(token)
    if claims.status_code == 498 or claims.status_code == 401:
        return make_response('Invalid Token', 498)

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

    id = fetch_user_email(email)["id"]
    if ast.literal_eval(claims.data.decode('utf-8'))["user_id"] != id:
        return make_response('Not authorized', 401)

    user = UserDTO(0, firstname, lastname, age, email, "", size,
                   weight, post, nYE, description, picture)
    user = update_user(user)
    if (user is not None):
        return make_response(user, 200)
    return make_response("User not found", 404)


@users_bp.route("/adresses", methods=["GET"])
@cross_origin()
def get_adress_user():

    email = request.args.get("email", default="", type=str)
    role = get_role(email)
    if (role is not None):
        user = fetch_user_adress(role, email)
        if (user is not None):
            return make_response(user, 200)
    return make_response("", 404)


@users_bp.route("/applyClub", methods=["POST"])
@cross_origin()
def apply_for_club():
    email_user = request.json.get('email_user')
    email_club = request.json.get('email_club')
    apply_for_club_user(email_user, email_club)
    return "Request send"


@users_bp.route("/userClub", methods=["GET"])
@cross_origin()
def get_club():
    email_user = request.args.get("email_user", default="", type=str)
    return get_user_club(email_user)


@users_bp.route("/userSport", methods=["GET"])
@cross_origin()
def get_sport():
    email_user = request.args.get("email_user", default="", type=str)
    return get_user_sport(email_user)


@users_bp.route("/leaveClub", methods=["DELETE"])
@cross_origin()
def leave_club_player():
    email_user = request.json.get('email_user')
    email_club = request.json.get('email_club')
    leave_club(email_user, email_club)
    return "Request leave successfully"


@users_bp.route("/isMember", methods=["GET"])
@cross_origin()
def check_is_member():
    email_user = request.args.get("email_user", default="", type=str)
    if (is_member(email_user)):
        return "Is member"
    else:
        return "Not a member"


@users_bp.route("/searchUser", methods=["GET"])
@cross_origin()
def serach_user():
    sport = request.args.get("sport", default="", type=str)
    role = request.args.get("role", default="", type=str)
    age = request.args.get("age", default=0, type=int)
    country = request.args.get("country", default="", type=str)
    city = request.args.get("city", default="", type=str)
    name = request.args.get("name", default="", type=str)
    print("befor")
    return search_user_data(role, sport, age, country, city, name)
