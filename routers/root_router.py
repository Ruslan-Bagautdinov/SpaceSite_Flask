from flask import Blueprint, render_template, session, request

from templates.icons import HI_ICON
from tools.functions import load_unsplash_photo

root_bp = Blueprint('root', __name__)


@root_bp.route('/', methods=['GET', 'POST'])
def root():
    top_message = session.get('top_message', None)

    if top_message is None:
        if request.environ.get('current_user'):
            current_user = request.environ['current_user']
            text = f"Hello, {current_user.role} {current_user.username}!"
        else:
            text = "Welcome to our site!"
        top_message = {
            "class": "alert alert-light rounded",
            "icon": HI_ICON,
            "text": text
        }
    else:
        session.pop('top_message', None)

    unsplash_photo = load_unsplash_photo('universe galaxy cosmos')
    if unsplash_photo is None:
        unsplash_photo = '/static/img/default_unsplash.jpg'

    return render_template('root.html',
                           top_message=top_message,
                           unsplash_photo=unsplash_photo)
