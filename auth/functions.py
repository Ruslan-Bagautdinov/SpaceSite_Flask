from flask import (
    redirect,
    session,
    url_for
)
from flask_jwt_extended import (
    set_refresh_cookies,
    create_refresh_token
)
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    get_jwt_identity,
    get_jwt,
)
from flask import make_response

from datetime import datetime, timedelta, timezone

from templates.icons import WARNING_ICON


def redirect_authenticated_user(username: str,
                                redirect_uri: str = "root.root"):

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    response = make_response(redirect(url_for(redirect_uri)))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    response.set_cookie('username', username)
    return response


def redirect_not_authenticated_user():
    print('you are not authenticated')
    top_message = {
            "class": "alert alert-danger rounded",
            "icon": WARNING_ICON,
            "text": 'Please, login again',
        }
    session['top_message'] = top_message
    return redirect(url_for('auth.logout', path='auth.login'))


def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = (now + timedelta(minutes=1)).timestamp()
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return redirect_not_authenticated_user()


def redirect_with_message(message_class: str,
                          message_icon: str,
                          message_text: str,
                          endpoint: str):
    top_message = {
        "class": message_class,
        "icon": message_icon,
        "text": message_text,
    }
    session['top_message'] = top_message
    return redirect(url_for(endpoint))
