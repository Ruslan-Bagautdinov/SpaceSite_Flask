from flask import (
    redirect,
    session,
    url_for,
    make_response
)
from flask_jwt_extended import (
    set_refresh_cookies,
    create_refresh_token
)
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies
)


from tools.functions import redirect_with_message
from templates.icons import WARNING_ICON


def redirect_not_authenticated_user():
    return redirect_with_message(
        message_class="alert alert-danger rounded",
        message_icon=WARNING_ICON,
        message_text='Please, login again',
        logout=True
    )


def redirect_authenticated_user(username: str,
                                redirect_uri: str = "root.root"):

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    response = make_response(redirect(url_for(redirect_uri)))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    response.set_cookie('username', username)
    return response



