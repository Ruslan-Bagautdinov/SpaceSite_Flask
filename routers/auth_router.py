from flask import (
    Blueprint,
    request,
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
    set_refresh_cookies,
    create_refresh_token,
    get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


from database.models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if username is None or password is None:
            return jsonify({"msg": "Missing username or password"}), 400
        if User.query.filter_by(username=username).first() is not None:
            return jsonify({"msg": "User already exists"}), 400
        user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "User created successfully"}), 201
    data = {'username': request.cookies.get('username')}
    return render_template('auth/register.html', data=data)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password_hash, password):
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        resp = make_response(jsonify({'login': True}))
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200
    data = {'username': request.cookies.get('username')}
    return render_template('auth/login.html', data=data)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the new access token as a cookie
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


@auth_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.datetime.now(datetime.timezone.utc)
        target_timestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response
