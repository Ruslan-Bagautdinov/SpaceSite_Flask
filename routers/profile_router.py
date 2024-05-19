from flask import (Blueprint,
                   session,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash
                   )
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity
                                )

from werkzeug.utils import secure_filename
import os
from icecream import ic

from config import IMAGE_DIR
from auth.functions import refresh_expiring_jwts, redirect_with_message
from database.models import db, User, UserProfile
from database.crud import get_user, get_user_by_username, get_user_profile
from tools.functions import read_and_encode_photo, save_upload_file, allowed_file, error_message, ok_message
from templates.icons import WARNING_ICON


user_bp = Blueprint('user', __name__)


@user_bp.route('/me', methods=['GET'])
@jwt_required(refresh=True)
def get_me():
    try:
        current_user = get_jwt_identity()
        user = get_user_by_username(current_user)

        if user is None:
            return error_message('User not found!')

        user_id = user.id
        return redirect(f'/user/profile/{user_id}')

    except Exception as e:
        return error_message(str(e))

@user_bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required(refresh=True)
def get_profile(user_id):

    result_user = get_user(user_id=user_id)
    result_profile = get_user_profile(user_id=user_id)

    csrf_token = session.get('csrf_token', None)

    if not result_user or not result_profile:
        return error_message('User not found!')

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

    return render_template('user/profile.html', username=result_user.username, profile=profile, csrf_token=csrf_token)


@user_bp.route('/profile/<int:user_id>/update', methods=['POST'])
@jwt_required(refresh=True)
def update_profile(user_id):

    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    phone_number = request.form.get('phone_number', None)
    photo = request.files.get('photo', None)
    ass_size = request.form.get('ass_size', None)

    ic(first_name, last_name, phone_number, photo, ass_size)

    user_profile = get_user_profile(user_id=user_id)

    ic(photo)

    if not user_profile:
        return error_message('User not found!')

    previous_photo_path = user_profile.photo

    ic(previous_photo_path)

    if photo and photo.filename != '':
        if not allowed_file(photo.filename):
            return error_message("File must be an image", "root.root")

        filename = secure_filename(photo.filename)
        destination = os.path.join(IMAGE_DIR, filename)
        save_upload_file(photo, destination)
        user_profile.photo = destination

        if previous_photo_path and os.path.exists(previous_photo_path):
            os.remove(previous_photo_path)

    else:
        user_profile.photo = previous_photo_path

    user_profile.first_name = first_name
    user_profile.last_name = last_name
    user_profile.phone_number = phone_number
    user_profile.ass_size = ass_size

    db.session.commit()

    return ok_message("Saved successfully profile: ")


@user_bp.after_request
@jwt_required(refresh=True)
def refresh_access(response):
    return refresh_expiring_jwts(response)



