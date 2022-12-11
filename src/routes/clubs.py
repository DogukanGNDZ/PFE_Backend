from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.ClubDTO import *
from src.data.ClubToDatabase import *
import uuid
import bcrypt
import datetime

clubs_bp = Blueprint("clubs", __name__, url_prefix="/clubs")

# generate a new id


def generate_id():
    return str(uuid.uuid4())


@clubs_bp.route("", methods=["GET"])
def get_all_clubs():
    id = request.args.get("id", default=1, type=int)
    if (id == 1):
        return fetch_all_clubs()
    return fetch_club(id)


@clubs_bp.route("/register", methods=["POST"])
@cross_origin()
def register():
    password = request.json.get('password')
    byte_pwd = password.encode('UTF-8')
    pwd_hash = bcrypt.hashpw(byte_pwd, bcrypt.gensalt())
    name = request.json.get('name')
    email = request.json.get('email')
    club = ClubDTO(generate_id(), name, email, pwd_hash,
                   "", 0, datetime.datetime.now(), "")
    return create_club(club)


@clubs_bp.route("/memberRequests", methods=["GET"])
@cross_origin()
def get_member_request():
    email_club = request.args.get("email_club", default="", type=str)
    role = request.args.get("role", default="", type=str)
    if (role == "player"):
        return get_all_request_join_users(email_club)
    else:
        return get_all_request_join_coach(email_club)


@clubs_bp.route("/members", methods=["GET"])
@cross_origin()
def get_members():
    email_club = request.args.get("email_club", default="", type=str)
    role = request.args.get("role", default="", type=str)
    if (role == "player"):
        return get_all_players(email_club)
    else:
        return get_all_coachs(email_club)


@clubs_bp.route("/acceptNewMember", methods=["POST"])
@cross_origin()
def accept_member():
    email_member = request.json.get('email_member')
    role = request.json.get('role')
    email_club = request.json.get('email_club')
    accept_new_member(email_club, email_member, role)
    return "Member accepted"


@clubs_bp.route("/removeMember", methods=["DELETE"])
@cross_origin()
def remove_member_club():
    email_member = request.json.get('email_member')
    email_club = request.json.get('email_club')
    role = request.json.get('role')
    remove_member(email_club, email_member, role)
    return "Member remove"
