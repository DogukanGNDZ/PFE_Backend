from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.AdressDTO import *
from src.data.AdressToDatabase import *
from src.routes.auth import get_role
import uuid

adresses_bp = Blueprint("adresses", __name__, url_prefix="/adresses")


@adresses_bp.route("", methods=["GET"])
def get_all_adresses():
    id = request.args.get("id", default="", type=str)
    if (id == ""):
        return fetch_all_adress()
    return fetch_adress(id)

# generate a new id


def generate_id():
    return str(uuid.uuid4())


@adresses_bp.route("/create", methods=["POST"])
@cross_origin()
def create_adress():
    # Get the values from the request
    street = request.json.get('street')
    number = request.json.get('number')
    city = request.json.get('city')
    country = request.json.get('country')
    email = request.json.get('email')
    role = get_role(email)
    idOldAdress = request.json.get('idOldAdress')
    adress = AdressDTO(generate_id(), street, number, city, country)
    return create_adress_data(adress, email, role, idOldAdress)
