from flask import Blueprint, redirect, session, url_for, render_template, request, make_response
from flask_jwt_extended import unset_jwt_cookies
from werkzeug.security import check_password_hash

from auth.utils import redirect_authenticated_user
from database.crud import get_user_by_username, create_new_user
from templates.icons import USER_REGISTER_ICON
from tools.functions import error_message

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if get_user_by_username(username=username) is not None:
            return error_message(f"Username {username} is already registered!", endpoint='auth.register')

        create_new_user(username=username, email=email, password=password)

        top_message = {
            "class": "alert alert-info rounded",
            "icon": USER_REGISTER_ICON,
            "text": f"User {username} has been created"
        }
        session['top_message'] = top_message
        return redirect_authenticated_user(username, 'root.root')

    top_message = session.get('top_message', None)
    if top_message:
        session.pop('top_message', None)

    return render_template('auth/register.html', top_message=top_message)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        user = get_user_by_username(username=username)

        if user is None or not check_password_hash(user.password_hash, password):
            return error_message(message="Incorrect username or password!")

        top_message = {
            "class": "alert alert-info rounded",
            "icon": USER_REGISTER_ICON,
            "text": f"You are logged in as {user.role} with the account: {username}"
        }
        session['top_message'] = top_message
        return redirect_authenticated_user(username, 'root.root')

    top_message = session.get('top_message', None)
    if top_message:
        session.pop('top_message', None)

    return render_template('auth/login.html', top_message=top_message)


@auth_bp.route('/logout', methods=['GET'])
def logout():
    path = request.args.get('path', 'root.root')
    resp = make_response(redirect(url_for(path)))
    unset_jwt_cookies(resp)
    resp.set_cookie('username', '', expires=0)
    return resp
