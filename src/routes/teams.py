from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.TeamDTO import *
from src.data.TeamToDatabase import *
import uuid

teams_bp = Blueprint("teams", __name__, url_prefix="/teams")


@teams_bp.route("", methods=["GET"])
def get_all_teams():
    id = request.args.get("id", default=1, type=str)
    if (id == 1):
        return fetch_all_teams()

    team = fetch_team(id)
    if (team is not None):
        return make_response(team, 200)
    return make_response("Team not found", 404)
# generate a new id


def generate_id():
    return str(uuid.uuid4())


@teams_bp.route("/create", methods=["POST"])
@cross_origin()
def create():
    # Get the values from the request
    street = request.json.get('category')
    email_club = request.json.get('email_club')
    team = TeamDTO(generate_id(), street, 0)
    return create_team(team, email_club)


@teams_bp.route("/add", methods=["PUT"])
@cross_origin()
def put_player():

    player = request.json.get('player')
    team = request.json.get('team')

    if (add_player(team, player)):
        return make_response("", 200)
    else:
        return make_response("", 404)


@teams_bp.route("/remove", methods=["DELETE"])
@cross_origin()
def delete_player():

    player = request.json.get('player')
    team = request.json.get('team')

    if (remove_player(team, player)):
        return make_response("", 200)
    return make_response("", 404)


@teams_bp.route("/setCoach", methods=["PUT"])
@cross_origin()
def put_coach():

    coach = request.json.get('coach')
    team = request.json.get('team')

    if (add_coach(team, coach)):
        return make_response("", 200)
    return make_response("", 404)


@teams_bp.route("/getCoach", methods=["GET"])
@cross_origin()
def get_coach():

    team = request.args.get("id_team", default="", type=str)

    coach = fetch_coach(team)

    if (coach is not None):
        return make_response(coach, 200)
    return make_response("Pas coach", 200)


@ teams_bp.route("/updateCategory", methods=["PUT"])
@ cross_origin()
def update_category():
    team = request.json.get('team')
    category = request.json.get('category')
    team = update_category_data(team, category)

    if (team is not None):
        return make_response(team, 200)
    return make_response("", 404)


@ teams_bp.route("/teamsPlayer", methods=["GET"])
@ cross_origin()
def get_players_team():
    id = request.args.get("id_team", default="", type=str)
    return get_team_player_data(id)
