import os

from flask import (Blueprint,
                   session,
                   render_template,
                   request,
                   redirect
                   )
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity
                                )
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from app_config import IMAGE_DIR
from database.crud import (get_user,
                           get_user_by_username,
                           get_user_profile,
                           update_user_profile,
                           delete_user,
                           get_user_posts,
                           create_post,
                           get_post,
                           update_post,
                           delete_post
                           )
from templates.icons import USER_DELETE_ICON
from tools.functions import (read_and_encode_photo,
                             save_file_with_uuid,
                             allowed_file,
                             error_message,
                             ok_message
                             )

user_bp = Blueprint('user', __name__)


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    try:
        current_user = get_jwt_identity()
        user = get_user_by_username(current_user)

        if user is None:
            return error_message('User not found!')

        user_id = user.id
        response = redirect(f'/user/profile/{user_id}')
        return response

    except Exception as e:
        return error_message(str(e))


@user_bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required()
def profile(user_id):
    top_message = session.get('top_message', None)
    if top_message:
        session.pop('top_message', None)

    result_user = get_user(user_id=user_id)
    result_profile = get_user_profile(user_id=user_id)

    csrf_token = session.get('csrf_token', None)

    if not result_user or not result_profile:
        return error_message('User not found!')

    profile_for_page = {
        "user_id": result_user.id,
        'username': result_user.username,
        'email': result_user.email,
        "first_name": result_profile.first_name,
        "last_name": result_profile.last_name,
        'phone_number': result_profile.phone_number,
        'user_age': result_profile.user_age,
        'role': result_user.role
    }

    default_avatar_path = "static/img/default_avatar.jpg"
    if result_profile.user_photo and os.path.exists(result_profile.user_photo):
        photo_base64 = read_and_encode_photo(result_profile.user_photo)
        if photo_base64:
            profile_for_page['user_photo'] = photo_base64
        else:
            default_avatar_base64 = read_and_encode_photo(default_avatar_path)
            profile_for_page['user_photo'] = default_avatar_base64
    else:
        default_avatar_base64 = read_and_encode_photo(default_avatar_path)
        profile_for_page['user_photo'] = default_avatar_base64

    response = render_template('user/profile.html',
                               username=result_user.username,
                               profile=profile_for_page,
                               csrf_token=csrf_token,
                               top_message=top_message
                               )
    return response


@user_bp.route('/profile/<int:user_id>/update', methods=['POST'])
@jwt_required()
def profile_update(user_id):
    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    phone_number = request.form.get('phone_number', None)
    user_photo = request.files.get('user_photo', None)
    user_age = request.form.get('user_age', None)
    user_age = int(user_age) if user_age else None

    user = get_user(user_id=user_id)
    user_profile = get_user_profile(user_id=user_id)

    if not user or not user_profile:
        return error_message('User not found!')

    previous_photo_path = user_profile.user_photo

    if user_photo and user_photo.filename != '':
        if not allowed_file(user_photo.filename):
            return error_message('File must be an image!',
                                 endpoint="user.me")

        photo = save_file_with_uuid(user_photo, IMAGE_DIR)

        if previous_photo_path and os.path.exists(previous_photo_path):
            os.remove(previous_photo_path)

    else:
        photo = previous_photo_path

    update = update_user_profile(user_id=user_id,
                                 first_name=first_name,
                                 last_name=last_name,
                                 phone_number=phone_number,
                                 user_age=user_age,
                                 user_photo=photo)
    if update:
        return ok_message(f"{user.username}, Your profile has been updated!",
                          endpoint="user.me")
    else:
        return error_message('User not found!')


@user_bp.route('/profile/<int:user_id>/delete', methods=['GET', 'POST'])
@jwt_required()
def profile_delete(user_id):
    result_user = get_user(user_id=user_id)
    user_profile = get_user_profile(user_id)
    previous_photo_path = user_profile.user_photo

    if request.method == 'POST':
        password = request.form.get('password', None)
        if not check_password_hash(result_user.password_hash, password):
            return error_message('Incorrect password!')

        if delete_user(user_id):
            if previous_photo_path and os.path.exists(previous_photo_path):
                os.remove(previous_photo_path)

            return error_message(f"{result_user.username} has been deleted!",
                                 icon=USER_DELETE_ICON,
                                 endpoint="auth.logout")
        else:
            return error_message(message=f"User {result_user.username} not found!")

    csrf_token = session.get('csrf_token', None)
    response = render_template('user/confirm_delete.html',
                               username=result_user.username,
                               user_id=user_id,
                               csrf_token=csrf_token)
    return response


@user_bp.route('/posts', methods=['GET'])
@jwt_required()
def user_posts():
    current_user = get_jwt_identity()
    user = get_user_by_username(current_user)
    page = request.args.get('page', 1, type=int)
    per_page = 15
    posts = get_user_posts(user.id, page=page, per_page=per_page)
    total_posts = get_user_posts(user.id, count=True)
    pagination = {
        'page': page,
        'per_page': per_page,
        'total': total_posts,
        'pages': (total_posts // per_page) + (1 if total_posts % per_page else 0)
    }
    return render_template('user/posts.html', posts=posts, current_user=user, pagination=pagination)


@user_bp.route('/post/create', methods=['GET', 'POST'])
@jwt_required()
def create_post_route():
    if request.method == 'POST':
        content = request.form.get('content')
        current_user = get_jwt_identity()
        user = get_user_by_username(current_user)
        create_post(user.id, content)
        return ok_message('Post created successfully', endpoint='user.user_posts')
    return render_template('user/create_post.html')


@user_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@jwt_required()
def edit_post_route(post_id):
    post = get_post(post_id)
    if not post:
        return error_message('Post not found')
    if request.method == 'POST':
        content = request.form.get('content')
        update_post(post_id, content)
        return ok_message('Post updated successfully', endpoint='user.user_posts')
    current_user = get_jwt_identity()
    user = get_user_by_username(current_user)
    return render_template('user/edit_post.html', post=post, current_user=user)


@user_bp.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@jwt_required()
def delete_post_route(post_id):
    post = get_post(post_id)
    if not post:
        return error_message('Post not found')
    if request.method == 'POST':
        delete_post(post_id)
        return ok_message('Post deleted successfully', endpoint='user.user_posts')
    current_user = get_jwt_identity()
    user = get_user_by_username(current_user)
    return render_template('user/edit_post.html', post=post, current_user=user)
