from flask import redirect, url_for, make_response
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt_identity,
                                set_access_cookies,
                                set_refresh_cookies)
from jwt import (decode,
                 ExpiredSignatureError,
                 InvalidTokenError)

from config import SECRET_KEY, ALGORITHM
from database.crud import get_user_by_username


def decode_token(token):
    return decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def verify_token(token, token_type):
    try:
        payload = decode_token(token)
        if payload['type'] == token_type:
            return payload['username'], payload['role']
        raise InvalidTokenError("Invalid token type")
    except ExpiredSignatureError:
        raise ExpiredSignatureError("Token expired")
    except InvalidTokenError:
        raise InvalidTokenError("Invalid token")


def refresh_access_token(refresh_token):
    try:
        payload = decode_token(refresh_token)
        if payload['type'] == 'refresh_token':
            username = payload['username']
            role = payload['role']
            additional_claims = {
                'role': role
            }
            return create_access_token(identity=username, additional_claims=additional_claims)
        raise InvalidTokenError("Invalid token type")
    except ExpiredSignatureError:
        raise ExpiredSignatureError("Refresh token expired")
    except InvalidTokenError:
        raise InvalidTokenError("Invalid refresh token")


def get_current_user():
    try:
        current_user = get_jwt_identity()
        return get_user_by_username(current_user) if current_user else None
    except:
        return None


def redirect_authenticated_user(username: str, redirect_uri: str = "root.root"):
    user = get_user_by_username(username)
    if not user:
        return redirect(url_for('auth.login'))

    additional_claims = {
        'role': user.role
    }

    access_token = create_access_token(identity=username, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=username, additional_claims=additional_claims)
    response = make_response(redirect(url_for(redirect_uri)))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    response.set_cookie('username', username)
    return response


def redirect_not_authenticated_user():
    return redirect(url_for('auth.login'))
