import os

from flask import Blueprint, session, render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from config import IMAGE_DIR
from database.crud import (get_all_users,
                           get_user,
                           get_user_by_username,
                           update_user_role,
                           get_user_profile,
                           update_user_profile,
                           delete_user,
                           get_user_posts,
                           get_post,
                           update_post,
                           delete_post
                           )
from templates.icons import USER_DELETE_ICON
from tools.functions import (save_upload_file,
                             allowed_file,
                             error_message,
                             read_and_encode_photo
                             )

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def all_users():
    users = get_all_users()
    return render_template('admin/all_users.html', users=users)


@admin_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def user_profile(user_id):
    user = get_user(user_id=user_id)
    if not user:
        return error_message('User not found!')

    user_profile = get_user_profile(user_id=user_id)
    if not user_profile:
        return error_message('User profile not found!')

    profile_for_page = {
        "user_id": user.id,
        'username': user.username,
        'email': user.email,
        "first_name": user_profile.first_name,
        "last_name": user_profile.last_name,
        'phone_number': user_profile.phone_number,
        'user_age': user_profile.user_age,
        'role': user.role
    }

    default_avatar_path = "static/img/default_avatar.jpg"
    if user_profile.user_photo and os.path.exists(user_profile.user_photo):
        photo_base64 = read_and_encode_photo(user_profile.user_photo)
        if photo_base64:
            profile_for_page['user_photo'] = photo_base64
        else:
            default_avatar_base64 = read_and_encode_photo(default_avatar_path)
            profile_for_page['user_photo'] = default_avatar_base64
    else:
        default_avatar_base64 = read_and_encode_photo(default_avatar_path)
        profile_for_page['user_photo'] = default_avatar_base64

    current_user = get_jwt_identity()
    current_user_obj = get_user_by_username(current_user)

    return render_template('user/profile.html', profile=profile_for_page, current_user=current_user_obj)


@admin_bp.route('/user/<int:user_id>/update', methods=['POST'])
@jwt_required()
def update_user(user_id):
    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    phone_number = request.form.get('phone_number', None)
    user_photo = request.files.get('user_photo', None)
    user_age = request.form.get('user_age', None)
    user_age = int(user_age) if user_age else None
    role = request.form.get('role', 'user')

    user = get_user(user_id=user_id)
    if not user:
        return error_message('User not found!')

    user_profile = get_user_profile(user_id=user_id)
    previous_photo_path = user_profile.user_photo

    if user_photo and user_photo.filename != '':
        if not allowed_file(user_photo.filename):
            return error_message('File must be an image!')

        filename = secure_filename(user_photo.filename)
        destination = os.path.join(IMAGE_DIR, filename)
        save_upload_file(user_photo, destination)
        photo = destination

        if previous_photo_path and os.path.exists(previous_photo_path):
            os.remove(previous_photo_path)

    else:
        photo = previous_photo_path

    update_profile = update_user_profile(user_id=user_id,
                                         first_name=first_name,
                                         last_name=last_name,
                                         phone_number=phone_number,
                                         user_age=user_age,
                                         user_photo=photo)
    update_role = update_user_role(user_id=user_id, role=role)

    if update_profile and update_role:
        return redirect(url_for('admin.all_users'))
    else:
        return error_message('Failed to update user profile.')


@admin_bp.route('/user/<int:user_id>/delete', methods=['GET', 'POST'])
@jwt_required()
def profile_delete(user_id):
    current_user = get_jwt_identity()
    current_user_obj = get_user_by_username(current_user)
    result_user = get_user(user_id=user_id)
    user_profile = get_user_profile(user_id)
    previous_photo_path = user_profile.user_photo

    if request.method == 'POST':
        if current_user_obj.id == user_id:
            password = request.form.get('password', None)
            if not check_password_hash(current_user_obj.password_hash, password):
                return error_message('Incorrect password!')

        if delete_user(user_id):
            if previous_photo_path and os.path.exists(previous_photo_path):
                os.remove(previous_photo_path)

            if current_user_obj.id == user_id:
                return error_message(f"{result_user.username} has been deleted!",
                                     icon=USER_DELETE_ICON,
                                     endpoint="auth.logout")
            else:
                return redirect(url_for('admin.all_users'))
        else:
            return error_message(message=f"User {result_user.username} not found!")

    csrf_token = session.get('csrf_token', None)
    response = render_template('user/confirm_delete.html',
                               username=result_user.username,
                               user_id=user_id,
                               csrf_token=csrf_token)
    return response


@admin_bp.route('/user/<int:user_id>/posts', methods=['GET'])
@jwt_required()
def user_posts(user_id):
    user = get_user(user_id=user_id)
    if not user:
        return error_message('User not found!')

    posts = get_user_posts(user_id)
    current_user = get_jwt_identity()
    current_user_obj = get_user_by_username(current_user)
    return render_template('user/posts.html', posts=posts, user_id=user_id, current_user=current_user_obj)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@jwt_required()
def edit_post(post_id):
    post = get_post(post_id)
    if not post:
        return error_message('Post not found')
    if request.method == 'POST':
        content = request.form.get('content')
        update_post(post_id, content)
        return redirect(url_for('admin.user_posts', user_id=post.user_id))
    current_user = get_jwt_identity()
    user = get_user_by_username(current_user)
    return render_template('user/edit_post.html', post=post, current_user=user)


@admin_bp.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@jwt_required()
def delete_user_post(post_id):
    post = get_post(post_id)
    if not post:
        return error_message('Post not found')
    if request.method == 'POST':
        if delete_post(post_id):  # Call the delete_post function from crud.py
            return redirect(url_for('admin.user_posts', user_id=post.user_id))
        else:
            return error_message('Failed to delete post')
    current_user = get_jwt_identity()
    user = get_user_by_username(current_user)
    return render_template('user/edit_post.html', post=post, current_user=user)
