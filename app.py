from flask import Flask
from flask_jwt_extended import JWTManager
from jwt.exceptions import ExpiredSignatureError

from datetime import timedelta
import os


from config import SECRET_KEY, BASE_DIR
from database.models import db
from routers.root_router import root_bp
from routers.auth_router import auth_bp
from routers.profile_router import user_bp

from auth.functions import redirect_not_authenticated_user


app = Flask(__name__)

database_file = f"sqlite:///{os.path.join(BASE_DIR, 'spacesite_flask.db')}"
app.secret_key = SECRET_KEY


app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)


app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(root_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')


@app.errorhandler(ExpiredSignatureError)
def handle_expired_token(error):
    print('You are not authenticated')
    return redirect_not_authenticated_user()


with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
