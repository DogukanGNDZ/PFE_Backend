from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from dotenv import load_dotenv
from src.dto.UserDTO import *
from src.data.UserToDatabase import *
import jwt
import datetime
import os

load_dotenv()
KEY = os.getenv("KEYJWT")

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def generate_jwt(user_id):
    # Create the payload with the user's ID and an expiration date
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    # Sign the JWT using a secret key
    # do not forget to put this key in the env filee
    jwt_token = jwt.encode(payload, KEY)
    return jwt_token


@auth_bp.route("/login", methods=["POST"])
@cross_origin()
def login():
    password = request.json.get('password')
    byte_pwd = password.encode('UTF-8')
    email = request.json.get('email')
    if check_user(byte_pwd, email):
        get_user = fetch_user_email(email)
        print(get_user)
        return generate_jwt(get_user["id"])
    else:
        response = make_response("Wrong password", 400)
        return response


@auth_bp.route("/confirm_token", methods=['POST'])
@cross_origin()
def confirm_token():
    # Get the token from the request
    token = request.json['token']
    # Validate the token
    try:
        # Decode the token using your secret key
        decoded_token = jwt.decode(token, KEY, 'HS256')
        # The token is valid
        response = make_response("Valid token", 200)
        return response
    # The token has expired
    except jwt.ExpiredSignatureError:
        response = make_response("Token has expired", 401)
        return response
    # The token is invalid
    except jwt.InvalidTokenError:
        response = make_response("Token is invalid", 498)
        return response


def authorize(token: str):
    try:
        # Decode the token using your secret key
        decoded_token = jwt.decode(token, KEY, 'HS256')
        # The token is valid
        response = make_response(decoded_token, 200)
        return response
    # The token has expired
    except jwt.ExpiredSignatureError:
        response = make_response("Token has expired", 401)
        return response
    # The token is invalid
    except jwt.InvalidTokenError:
        response = make_response("Token is invalid", 498)
        return response


def get_role(email: str):
    return get_role_user(email)
