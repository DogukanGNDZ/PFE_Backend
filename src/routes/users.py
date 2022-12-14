from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from azure.storage.blob import BlobServiceClient
from src.dto.UserDTO import *
from src.dto.NotificationDTO import *
from src.data.UserToDatabase import *
from src.data.CoachToDatabase import update_coach
from src.data.ClubToDatabase import update_club
from src.dto.CoachDTO import *
from src.dto.ClubDTO import *
from src.data.AdressToDatabase import fetch_user_adress
from src.data.NotificationToDatabase import create_notification_data
from src.routes.auth import authorize, get_role
from dotenv import load_dotenv
import uuid
import bcrypt
import ast
import datetime
import os

load_dotenv()
KEYAZURE = os.getenv("STRINGAZURE")

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("", methods=["GET"])
@cross_origin()
def get_all_users():
    return fetch_all_users()


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
                   email, pwd_hash, 0, 0, "", 0, "", "", "")
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
                   weight, post, nYE, description, picture, "")
    user = update_user(user)
    if (user is not None):
        notification_user = NotificationDTO(
            generate_id(), "Votre profil a bien été modifié", datetime.datetime.now(), "active")
        create_notification_data(notification_user, "player", email)
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
    notification_player = NotificationDTO(generate_id(
    ), "Vous avez bien postulez pour un club", datetime.datetime.now(), "active")
    notification_club = NotificationDTO(
        generate_id(), "Nouvelle demande d'inscription : Player", datetime.datetime.now(), "active")
    create_notification_data(notification_club, "club", email_club)
    create_notification_data(notification_player, "player", email_user)
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

    message = "un joueur à quitté votre club, email joueur = " + email_user
    notification_user = NotificationDTO(
        generate_id(), "Vous avez quitté votre club", datetime.datetime.now(), "active")
    notification_club = NotificationDTO(
        generate_id(), message, datetime.datetime.now(), "active")
    create_notification_data(notification_user, "player", email_user)
    create_notification_data(notification_club, "club", email_club)

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
    return search_user_data(role, sport, age, country, city, name)


@users_bp.route("/uploadImage", methods=["POST"])
@cross_origin()
def upload_image():
    # Get the image file from the request
    token = request.headers.get('Authorize')
    claims = authorize(token)
    if claims.status_code == 498 or claims.status_code == 401:
        return make_response('Invalid Token', 498)

    id = ast.literal_eval(claims.data.decode('utf-8'))["user_id"]
    user = fetch_user(id)
    role = get_role(user["email"])
    image_file = request.files["image"]

    # Create a BlobServiceClient object to connect to your Azure Blob Storage account

    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str=KEYAZURE
    )
    # Create a container in your Azure Blob Storage account
    container_name = "imagess"
    container_client = blob_service_client.get_container_client(container_name)

    # Upload the image file to the container

    blob_name = image_file.filename+generate_id()+".png"
    if (role == "player"):
        userd = UserDTO(0, user["firstname"], user["lastname"], user["age"], user["email"], "", user["size"],
                        user["weight"], user["post"], user["number_year_experience"], user["description"], blob_name,"")
        update_user(userd)
    elif (role == "coach"):
        coachd = CoachDTO(0, user["firstname"], user["lastname"], user["age"], user["email"], "",
                          user["number_year_experience"], user["description"], blob_name, user["picture_banner"])
        update_coach(coachd)
    else:
        clubd = ClubDTO(0, user["name"], user["email"], "", user["description"],
                        user["number_teams"], user["creation_date"], blob_name, user["picture_banner"])
        update_club(clubd)
    blob_client = container_client.upload_blob(blob_name, image_file)

    return make_response("Image uploaded successfully", 200)


@users_bp.route("/uploadImageBanner", methods=["POST"])
@cross_origin()
def upload_image_banner():
    # Get the image file from the request
    token = request.headers.get('Authorize')
    claims = authorize(token)
    if claims.status_code == 498 or claims.status_code == 401:
        return make_response('Invalid Token', 498)

    id = ast.literal_eval(claims.data.decode('utf-8'))["user_id"]
    user = fetch_user(id)
    role = get_role(user["email"])
    image_file = request.files["image"]

    # Create a BlobServiceClient object to connect to your Azure Blob Storage account

    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str=KEYAZURE
    )
    # Create a container in your Azure Blob Storage account
    container_name = "imagess"
    container_client = blob_service_client.get_container_client(container_name)

    # Upload the image file to the container

    blob_name = image_file.filename+generate_id()+".png"
    if (role == "player"):
        userd = UserDTO(0, user["firstname"], user["lastname"], user["age"], user["email"], "", user["size"],
                        user["weight"], user["post"], user["number_year_experience"], user["description"], user["picture"], blob_name)
        update_user(userd)
    elif (role == "coach"):
        coachd = CoachDTO(0, user["firstname"], user["lastname"], user["age"], user["email"], "",
                          user["number_year_experience"], user["description"], user["picture"], blob_name)
        update_coach(coachd)
    else:
        clubd = ClubDTO(0, user["name"], user["email"], "", user["description"],
                        user["number_teams"], user["creation_date"], user["picture"], blob_name)
        update_club(clubd)
    blob_client = container_client.upload_blob(blob_name, image_file)

    return make_response("Image uploaded successfully", 200)
