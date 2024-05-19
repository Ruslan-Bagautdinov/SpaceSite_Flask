from flask import (
    Blueprint,
    request,
    redirect,
    session,
    url_for,
    render_template,
    jsonify,
    request,
    make_response)


from flask_jwt_extended import (get_jwt,
                                jwt_required,
                                get_jwt_identity,
                                create_access_token,
                                set_access_cookies,
                                verify_jwt_in_request,
                                decode_token)

from jwt.exceptions import ExpiredSignatureError

from sqlalchemy.orm.exc import NoResultFound
from icecream import ic
import os
from functools import wraps
from datetime import datetime, timedelta, timezone


from auth.user_auth import refresh_expiring_jwts
from database.models import User, UserProfile
from tools.tools import read_and_encode_photo
from templates.icons.icons import WARNING_ICON


user_bp = Blueprint('user', __name__)


from flask import request, redirect, url_for



@user_bp.route('/me', methods=['GET'])
@jwt_required(refresh=True)
def get_me():
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).one()
        user_id = user.id
        return redirect(f'/user/profile/{user_id}')

    except NoResultFound:
        top_message = {
            "class": "alert alert-danger rounded",
            "icon": WARNING_ICON,
            "text": 'User not found!'
        }
        session['top_message'] = top_message
        return redirect(url_for('auth.login'))

    except Exception as e:
        top_message = {
            "class": "alert alert-danger rounded",
            "icon": WARNING_ICON,
            "text": str(e)
        }
        session['top_message'] = top_message
        return redirect(url_for('auth.login'))


@user_bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required(refresh=True)
def get_profile(user_id):

    try:
        result_user = User.query.filter_by(id=user_id).one()
        result_profile = UserProfile.query.filter_by(id=user_id).one()
    except NoResultFound:
        top_message = {
            "class": "alert alert-danger rounded",
            "icon": WARNING_ICON,
            "text": 'User not found!'
        }
        session['top_message'] = top_message
        return redirect(url_for('auth.login'))

    profile = {
        "user_id": result_user.id,
        'username': result_user.username,
        'email': result_user.email,
        "first_name": result_profile.first_name,
        "last_name": result_profile.last_name,
        'phone_number': result_profile.phone_number,
        'ass_size': result_profile.ass_size
    }

    default_avatar_path = "static/img/default_avatar.jpg"
    if result_profile.photo and os.path.exists(result_profile.photo):
        photo_base64 = read_and_encode_photo(result_profile.photo)
        if photo_base64:
            profile['photo'] = photo_base64
        else:
            default_avatar_base64 = read_and_encode_photo(default_avatar_path)
            profile['photo'] = default_avatar_base64
    else:
        default_avatar_base64 = read_and_encode_photo(default_avatar_path)
        profile['photo'] = default_avatar_base64

    return render_template('user/profile.html', username=result_user.username, profile=profile)


@user_bp.route('/profile/<int:user_id>/update', methods=['POST'])
@jwt_required(refresh=True)
def update_profile(user_id):

    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    phone_number = request.form.get('phone_number', None)
    ass_size = request.form.get('ass_size', None)


@user_bp.after_request
def refresh_access(response):
    return refresh_expiring_jwts(response)



