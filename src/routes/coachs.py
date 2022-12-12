from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.CoachDTO import *
from src.data.CoachToDatabase import *
from src.data.UserToDatabase import *
import uuid
import bcrypt

coachs_bp = Blueprint("coachs", __name__, url_prefix="/coachs")

# generate a new id


def generate_id():
    return str(uuid.uuid4())


@coachs_bp.route("", methods=["GET"])
def get_all_coachs():
    id = request.args.get("id", default=1, type=int)
    if (id == 1):
        return fetch_all_coachs()
    return fetch_coach(id)


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
                     age, email, pwd_hash, 0, "", "")
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
    leave_club(email_coach, email_club)
    return "Request leave successfully"


@coachs_bp.route("/isMember", methods=["GET"])
@cross_origin()
def check_is_member():
    email_coach = request.args.get("email_coach", default="", type=str)
    if (is_member(email_coach)):
        return "Is member"
    else:
        return "Not a member"
