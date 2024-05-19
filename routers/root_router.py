from flask import (
    Blueprint,
    render_template,
    session,
    request)

from tools.functions import load_unsplash_photo
from templates.icons import HI_ICON

root_bp = Blueprint('root', __name__)


@root_bp.route('/', methods=['GET', 'POST'])
def root():

    top_message = session.get('top_message', None)
    username = request.cookies.get('username', None)
    print(username)

    if top_message is None:
        top_message = {
            "class": "alert alert-light rounded",
            "icon": HI_ICON,
            "text": f"Hello again, "
        }
    else:
        session.pop('top_message', None)

    unsplash_photo = load_unsplash_photo('universe galaxy cosmos')
    if unsplash_photo is None:
        unsplash_photo = '/static/img/default_unsplash.jpg'

    return render_template('root.html',
                           username=username,
                           top_message=top_message,
                           unsplash_photo=unsplash_photo)
