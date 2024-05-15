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
from templates.icons.icons import HI_ICON


root_bp = Blueprint('root', __name__)


@root_bp.route('/', methods=['GET'])
def root(top_message: dict = None):

    if top_message is None:
        top_message = {
            "class": "alert alert-light rounded",
            "icon": HI_ICON,
            "text": ", welcome to our website!"
        }

    data = {'username': request.cookies.get('username'),
            'top_message': top_message
            }
    return render_template('root.html', data=data)

