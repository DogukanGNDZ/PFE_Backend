from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.SportDTO import *
from src.data.SportToDatabase import *
import uuid

sports_bp = Blueprint("sports", __name__, url_prefix="/sports")


@sports_bp.route("", methods=["GET"])
def get_all_sports():
    id = request.args.get("id", default=1, type=int)
    if (id == 1):
        return fetch_all_sports()
    return fetch_sport(id)

# generate a new id


def generate_id():
    return str(uuid.uuid4())


@sports_bp.route("/create", methods=["POST"])
@cross_origin()
def create_sport():
    # Get the values from the request
    name = request.json.get('name')
    sport = SportDTO(generate_id(), name)
    return create_sport_data(sport)


@sports_bp.route("/addSport", methods=["PUT"])
@cross_origin()
def add_sport_user():
    name = request.json.get('name')
    role = request.json.get('role')
    email = request.json.get('email')
    nameOldSport = request.json.get('nameOldSport')
    if (update_sport(name, role, email, nameOldSport)):
        return "sport added successfully"
    else:
        response = make_response("Wrong data", 400)
        return response


@sports_bp.route("/userSport", methods=["GET"])
@cross_origin()
def get_adress_user():
    role = request.args.get("role", default="", type=str)
    email = request.args.get("email", default="", type=str)
    return fetch_user_sport(role, email)
