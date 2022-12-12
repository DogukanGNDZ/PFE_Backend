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
        generate_id(), content, datetime.datetime.now(), "active")
    return create_notification_data(notification, role, email)


@notifications_bp.route("/getNotifications", methods=["GET"])
@cross_origin()
def get_user_notif():
    email_user = request.args.get("email_user", default="", type=str)
    role = request.args.get("role", default="", type=str)
    return fetch_user_notification(role, email_user)


@notifications_bp.route("/removeAllNotifications", methods=["DELETE"])
@cross_origin()
def remove_all_notif():
    remove_all_notifications()
    return "all notifications removed"


@notifications_bp.route("/updateState", methods=["POST"])
@cross_origin()
def update_state_notif():
    id = request.json.get("id")
    return update_notification_etat(id)
