from flask import Blueprint, jsonify

users_bp = Blueprint("users",__name__,url_prefix="/users")

@users_bp.route("",methods=["GET"])
def get_all_users():
    all_users = [{"id": 1, "name": "bob"},{"id":1,"name":"Joe"}]
    return jsonify(all_users)