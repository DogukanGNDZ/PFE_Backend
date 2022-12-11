from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from src.dto.NotificationDTO import *
from src.data.NotificationToDatabase import *
import uuid

notifications_bp = Blueprint(
    "notifications", __name__, url_prefix="/notifications")


@notifications_bp.route("", methods=["GET"])
def get_all_notifications():
    id = request.args.get("id", default="", type=str)
    if (id == ""):
        return fetch_all_notification()
    return fetch_notification(id)

# generate a new id


def generate_id():
    return str(uuid.uuid4())


@notifications_bp.route("/create", methods=["POST"])
@cross_origin()
def create_notification():
    content = request.json.get("content")
    role = request.json.get("role")
    email = request.json.get("email")
    notification = NotificationDTO(
        generate_id(), content, datetime.datetime.now())
    return create_notification_data(notification, role, email)
