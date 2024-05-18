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

from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies,
    set_refresh_cookies,
    create_refresh_token,
    get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from icecream import ic

from database.models import db, User, UserProfile
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from auth.user_auth import redirect_authenticated_user
from templates.icons.icons import USER_REGISTER_ICON, WARNING_ICON


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not password or not email:
            top_message = {
                "class": "alert alert-danger rounded",
                "icon": WARNING_ICON,
                "text": "Please enter all required fields!"
            }
            session['top_message'] = top_message
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first() is not None:
            top_message = {
                "class": "alert alert-danger rounded",
                "icon": WARNING_ICON,
                "text": "User already exists!"
            }
            session['top_message'] = top_message
            return redirect(url_for('auth.register'))

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        new_user_profile = UserProfile(
            user_id=new_user.id,
            first_name=None,
            last_name=None,
            phone_number=None,
            photo=None,
            ass_size=None
        )
        db.session.add(new_user_profile)
        db.session.commit()

        top_message = {
            "class": "alert alert-info rounded",
            "icon": USER_REGISTER_ICON,
            "text": f"Account created:"
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
        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password_hash, password):
            top_message = {
                "class": "alert alert-danger rounded",
                "icon": WARNING_ICON,
                "text": "Bad username or password!"
            }
            session['top_message'] = top_message
            return redirect(url_for('auth.login'))

        top_message = {
            "class": "alert alert-info rounded",
            "icon": USER_REGISTER_ICON,
            "text": f"Access granted:"
        }
        session['top_message'] = top_message
        return redirect_authenticated_user(username, 'root.root')

    top_message = session.get('top_message', None)
    if top_message:
        session.pop('top_message', None)
    return render_template('auth/login.html', top_message=top_message)


@auth_bp.route('/logout', methods=['GET'])
def logout():

    resp = make_response(redirect(url_for('root.root')))
    unset_jwt_cookies(resp)
    resp.set_cookie('username', '', expires=0)
    return resp
