from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.ClubDTO import *
from src.data.ClubToDatabase import *
import uuid
import bcrypt

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
    id_manager = request.json.get('id_manager')
    club = ClubDTO(generate_id(), name, email, pwd_hash, id_manager)
    return create_club(club)
