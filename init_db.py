from alembic.config import Config
from werkzeug.security import generate_password_hash

from alembic import command
from app import app
from database.crud import create_new_user
from database.models import db, User


def init_db():
    with app.app_context():
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        db.create_all()

        if not User.query.filter_by(username='user').first():
            create_new_user('user', 'user@example.com', generate_password_hash('123'), 'user')

        if not User.query.filter_by(username='admin').first():
            create_new_user('admin', 'admin@example.com', generate_password_hash('123'), 'admin')


if __name__ == "__main__":
    init_db()
