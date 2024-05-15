from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)


@user_bp.route('/protected', methods=['GET'])
@jwt_required(refresh=True)
def protected():
    try:
        # Attempt to get the identity of the current user
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200
    except Exception as e:
        # If the access token is expired, this will raise an exception
        return jsonify({"msg": "Please log in again"}), 401
