from flask import Blueprint, render_template, session, request
from flask_paginate import Pagination, get_page_parameter

from database.crud import get_all_posts
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

    # Pagination logic
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    offset = (page - 1) * per_page
    total = len(get_all_posts())
    posts = get_all_posts()[offset:offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')

    return render_template('root.html',
                           top_message=top_message,
                           unsplash_photo=unsplash_photo,
                           posts=posts,
                           pagination=pagination)
