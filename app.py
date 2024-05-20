from flask import (Flask,
                   session,
                   request,
                   redirect,
                   url_for
                   )
from flask_jwt_extended import (JWTManager,
                                jwt_required,
                                get_jwt_identity,
                                create_access_token,
                                set_access_cookies
                                )
from jwt.exceptions import ExpiredSignatureError

from datetime import timedelta
import os


from config import (SECRET_KEY,
                    BASE_DIR,
                    ACCESS_TOKEN_EXPIRE_MINUTES,
                    REFRESH_TOKEN_EXPIRE_MINUTES
                    )
from database.models import db
from routers.root_router import root_bp
from routers.auth_router import auth_bp
from routers.user_router import user_bp

from auth.utils import redirect_not_authenticated_user


app = Flask(__name__)

database_file = f"sqlite:///{os.path.join(BASE_DIR, 'spacesite_flask.db')}"
app.secret_key = SECRET_KEY

app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)


app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(root_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')


@jwt_required(refresh=True)
def refresh_expiring_jwts():
    try:
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        next_url = session.pop('next_url', None)
        response = redirect(next_url or url_for('root.root'))
        set_access_cookies(response, access_token)
        return response
    except Exception as error:
        print(str(error))
        return redirect_not_authenticated_user()


@app.errorhandler(ExpiredSignatureError)
def handle_expired_token(error):
    print('app.errorhandler:' + str(error))
    session['next_url'] = request.path

    return refresh_expiring_jwts()


with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
