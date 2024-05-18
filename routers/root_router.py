from flask import (
    Blueprint,
    render_template,
    session,
    request)


from templates.icons.icons import HI_ICON

root_bp = Blueprint('root', __name__)


@root_bp.route('/', methods=['GET', 'POST'])
def root():

    top_message = session.get('top_message', None)
    username = request.cookies.get('username', None)

    if top_message is None:
        top_message = {
            "class": "alert alert-light rounded",
            "icon": HI_ICON,
            "text": f"Glad to see you again,"
        }
    else:
        session.pop('top_message', None)

    return render_template('root.html',
                           username=username,
                           top_message=top_message)
