import datetime
from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from src.data.NotificationToDatabase import create_notification_data
from src.dto.NotificationDTO import NotificationDTO

from src.dto.CoachDTO import *
from src.data.CoachToDatabase import *
from src.data.UserToDatabase import *
from src.routes.auth import authorize
import uuid
import ast
import bcrypt

coachs_bp = Blueprint("coachs", __name__, url_prefix="/coachs")

# generate a new id


def generate_id():
    return str(uuid.uuid4())


@coachs_bp.route("", methods=["GET"])
@cross_origin()
def get_all_coachs():
    id = request.args.get("id", default=1, type=int)
    if (id == 1):
        return fetch_all_coachs()

    coach = fetch_coach(id)
    if (coach is not None):
        return make_response(coach, 200)
    return make_response("Coach not found", 404)


@coachs_bp.route("/register", methods=["POST"])
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
    coach = CoachDTO(generate_id(), firstname, lastname,
                     age, email, pwd_hash, 0, "", "", "")
    if (check_mail(email)):
        return make_response("Email already use", 400)
    else:
        return create_coach(coach)


@coachs_bp.route("/applyClub", methods=["POST"])
@cross_origin()
def apply_for_club():
    email_coach = request.json.get('email_coach')
    email_club = request.json.get('email_club')
    apply_for_club_coach(email_coach, email_club)

    notification_coach = NotificationDTO(
        generate_id(), "Vous avez bien postulez pour un club", datetime.datetime.now(), "active")
    notification_club = NotificationDTO(
        generate_id(), "Nouvelle demande d'inscription : Coach", datetime.datetime.now(), "active")

    create_notification_data(notification_club, "club", email_club)
    create_notification_data(notification_coach, "coach", email_coach)

    return "Request send"


@coachs_bp.route("/coachClub", methods=["GET"])
@cross_origin()
def get_club():
    email_coach = request.args.get("email_coach", default="", type=str)
    return get_coach_club(email_coach)


@coachs_bp.route("/leaveClub", methods=["DELETE"])
@cross_origin()
def leave_club_coach():
    email_coach = request.json.get('email_coach')
    email_club = request.json.get('email_club')
    left = leave_club(email_coach, email_club)
    if (not left):
        return make_response("", 404)

    message = "un coach à quitté votre club, email coach = " + email_coach
    notification_user = NotificationDTO(
        generate_id(), "Vous avez quitté votre club", datetime.datetime.now(), "active")
    notification_club = NotificationDTO(
        generate_id(), message, datetime.datetime.now(), "active")

    create_notification_data(notification_user, "coach", email_coach)
    create_notification_data(notification_club, "club", email_club)

    return make_response("Request leave successfully", 200)


@coachs_bp.route("/isMember", methods=["GET"])
@cross_origin()
def check_is_member():
    email_coach = request.args.get("email_coach", default="", type=str)
    if (is_member(email_coach)):
        return "Is member"
    else:
        return "Not a member"


@coachs_bp.route("/update", methods=["PUT"])
@cross_origin()
def update_data_coach():
    token = request.headers.get('Authorize')
    claims = authorize(token)
    if claims.status_code == 498 or claims.status_code == 401:
        return make_response('Invalid Token', 498)

    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    age = request.json.get('age')
    nYE = request.json.get('number_year_experience')
    description = request.json.get('description')
    picture = request.json.get('picture')
    picture_banner = request.json.get('picture_banner')

    id = fetch_user_email(email)["id"]
    if ast.literal_eval(claims.data.decode('utf-8'))["user_id"] != id:
        return make_response('Not authorized', 401)

    user = CoachDTO(0, firstname, lastname, age, email,
                    "", nYE, description, picture, picture_banner)
    user = update_user(user)
    if (user is not None):
        notification_user = NotificationDTO(
            generate_id(), "Votre profil a bien été modifié", datetime.datetime.now(), "active")
        create_notification_data(notification_user, "coach", email)
        return make_response(user, 200)
    return make_response("User not found", 404)
