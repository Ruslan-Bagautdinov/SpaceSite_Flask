from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from routers.root_router import root_bp
from routers.auth_router import auth_bp
from routers.user_router import user_bp
from config import SECRET_KEY, BASE_DIR
from database.models import db
import os

app = Flask(__name__)

database_file = f"sqlite:///{os.path.join(BASE_DIR, 'spacesite_flask.db')}"

app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(root_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Create the database and tables
with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")

if __name__ == '__main__':
    app.run(debug=True)