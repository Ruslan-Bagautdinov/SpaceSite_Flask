from flask import request, redirect, url_for
from flask_jwt_extended import verify_jwt_in_request

from auth.utils import get_current_user, refresh_access_token

ignore_path = ["/login", "/logout"]
ignore_start = ["/docs", "/openapi.json"]


def jwt_middleware(app):
    @app.before_request
    def before_request():
        if any(request.path.startswith(start) for start in ignore_start):
            return
        if request.path in ignore_path:
            return

        try:
            verify_jwt_in_request()
            current_user = get_current_user()
            request.environ['current_user'] = current_user
        except:
            request.environ['current_user'] = None

        if request.path.startswith('/protected'):
            access_token = request.cookies.get("access_token")
            refresh_token = request.cookies.get("refresh_token")

            if access_token:
                try:
                    verify_jwt_in_request()
                except:
                    return handle_token_refresh(refresh_token)
            elif refresh_token:
                return handle_token_refresh(refresh_token)
            else:
                return redirect(url_for('auth.login'))

    def handle_token_refresh(refresh_token):
        try:
            new_access_token = refresh_access_token(refresh_token)
            response = redirect(request.path)
            response.set_cookie('access_token', new_access_token)
            if refresh_token:
                response.set_cookie('refresh_token', refresh_token)
            return response
        except:
            response = redirect(url_for('auth.login'))
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
