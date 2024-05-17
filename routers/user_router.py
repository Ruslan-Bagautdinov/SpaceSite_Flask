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


from flask_jwt_extended import (jwt_required,
                                get_jwt_identity,
                                verify_jwt_in_request)

from sqlalchemy.orm.exc import NoResultFound
from icecream import ic


from auth.user_auth import refresh_expiring_jwts
from database.models import User, UserProfile
from templates.icons.icons import WARNING_ICON


user_bp = Blueprint('user', __name__)


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    try:

        current_user = get_jwt_identity()

        user = User.query.filter_by(username=current_user).one()
        user_id = user.id
        return redirect(f'/user/profile/{user_id}')

    except NoResultFound:
        top_message = {
            "class": "alert alert-danger rounded",
            "icon": WARNING_ICON,
            "text": 'User not found!'
        }
        session['top_message'] = top_message
        return redirect(url_for('auth.login'))

    except Exception as e:
        top_message = {
            "class": "alert alert-danger rounded",
            "icon": WARNING_ICON,
            "text": str(e)
        }
        session['top_message'] = top_message
        return redirect(url_for('auth.login'))


@user_bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):

    profile = UserProfile.query.filter_by(id=user_id).one()

    return render_template('user/profile.html', profile=profile)



@user_bp.after_request
# @jwt_required()
def refresh_expiring_tokens(response):
    return refresh_expiring_jwts(response)
