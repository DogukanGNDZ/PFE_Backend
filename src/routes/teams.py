from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.TeamDTO import *
from src.data.TeamToDatabase import *
import uuid

teams_bp = Blueprint("teams", __name__, url_prefix="/teams")


@teams_bp.route("", methods=["GET"])
def get_all_teams():
    id = request.args.get("id", default=1, type=int)
    if (id == 1):
        return fetch_all_teams()
    return fetch_team(id)

# generate a new id


def generate_id():
    return str(uuid.uuid4())


@teams_bp.route("/create", methods=["POST"])
@cross_origin()
def create_team():
    # Get the values from the request
    street = request.json.get('category')
    team = TeamDTO(generate_id(), street, 0)
    return team
