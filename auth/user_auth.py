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
    verify_jwt_in_request,
    get_jwt_identity,
    create_access_token,
    get_jwt_identity,
    get_jwt_header,
    set_access_cookies,
    unset_jwt_cookies,
    set_refresh_cookies,
    create_refresh_token,
    get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from icecream import ic


from database.models import db, User
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from templates.icons.icons import WARNING_ICON



def redirect_authenticated_user(username: str,
                                redirect_uri: str = "root.root",
                                top_message: dict = None):

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    response = make_response(redirect(url_for(redirect_uri)))

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    response.set_cookie('username', username)

    session['top_message'] = top_message

    return response

#
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.datetime.now(datetime.timezone.utc)
#         target_timestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         return response


def refresh_expiring_jwts(response):

    try:
        # Check if the response is a redirect response
        # if response.status_code in (301, 302, 303, 305, 307):
        #     return response

        # Extract the JWT from the response
        jwt_data = get_jwt()
        # if jwt_data is None:
        #     # No JWT found, so no need to refresh tokens
        #     return response

        exp_timestamp = jwt_data["exp"]
        now = datetime.datetime.now(datetime.timezone.utc)
        target_timestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        if target_timestamp > exp_timestamp:
            # Access token is about to expire, so refresh it
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)

        refresh_exp_timestamp = jwt_data["exp"]
        refresh_now = datetime.datetime.now(datetime.timezone.utc)
        refresh_target_timestamp = datetime.datetime.timestamp(refresh_now + datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
        if refresh_target_timestamp > refresh_exp_timestamp:
            # Refresh token is about to expire, so refresh it
            refresh_token = create_refresh_token(identity=get_jwt_identity())
            set_refresh_cookies(response, refresh_token)

        return response

    except Exception as e:
        # Handle any exceptions that occur during token refreshing
        unset_jwt_cookies(response)
        session.clear()
        top_message = {
            "class": "alert alert-danger rounded",
            "icon": WARNING_ICON,
            "text": str(e)
        }
        session['top_message'] = top_message
        return redirect(url_for('auth.login'))
