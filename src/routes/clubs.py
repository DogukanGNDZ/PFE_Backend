from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.ClubDTO import *
from src.dto.NotificationDTO import *
from src.data.ClubToDatabase import *
from src.data.NotificationToDatabase import create_notification_data
import uuid
import bcrypt
import datetime
from src.data.UserToDatabase import *
from src.routes.auth import get_role

clubs_bp = Blueprint("clubs", __name__, url_prefix="/clubs")

# generate a new id


def generate_id():
    return str(uuid.uuid4())


@clubs_bp.route("", methods=["GET"])
def get_all_clubs():
    id = request.args.get("id", default=1, type=int)
    if (id == 1):
        return fetch_all_clubs()

    club = fetch_club(id)
    if(club is not None): return make_response(club, 200)
    return make_response("Club not found", 404)


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
    if (check_mail(email)):
        return make_response("Email already use", 400)
    else:
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
    role = get_role(email_member)
    email_club = request.json.get('email_club')
    accept_new_member(email_club, email_member, role)
    notification_user = NotificationDTO(
        generate_id(), "Vous avez été accepté par un club", datetime.datetime.now(), "active")
    create_notification_data(notification_user, role, email_member)
    return "Member accepted"


@clubs_bp.route("/removeMember", methods=["DELETE"])
@cross_origin()
def remove_member_club():
    email_member = request.json.get('email_member')
    email_club = request.json.get('email_club')
    role = get_role(email_member)
    remove_member(email_club, email_member, role)
    notification_user = NotificationDTO(
        generate_id(), "Vous avez été viré du votre club actuel", datetime.datetime.now(), "active")
    create_notification_data(notification_user, role, email_member)
    return "Member remove"


@clubs_bp.route("/removeAllClubs", methods=["DELETE"])
@cross_origin()
def del_all():
    remove_all_clubs()
    return "All remove"
