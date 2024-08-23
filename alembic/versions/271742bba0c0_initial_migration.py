"""initial_migration

Revision ID: 271742bba0c0
Revises: 
Create Date: 2024-08-23 19:16:50.841251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from database.models import User, UserProfile, Post


# revision identifiers, used by Alembic.
revision: str = '271742bba0c0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the engine and session
    engine = op.get_bind()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create the tables
    User.__table__.create(engine)
    UserProfile.__table__.create(engine)
    Post.__table__.create(engine)

    # Insert initial users and profiles with the provided hashed passwords
    hashed_password = generate_password_hash('123')
    user_user = User(username='user', email='user@example.com', password_hash=hashed_password, role='user')
    user_admin = User(username='admin', email='admin@example.com', password_hash=hashed_password, role='admin')

    session.add(user_user)
    session.add(user_admin)
    session.commit()

    user_profile_user = UserProfile(user_id=user_user.id)
    user_profile_admin = UserProfile(user_id=user_admin.id)

    session.add(user_profile_user)
    session.add(user_profile_admin)
    session.commit()


def downgrade():
    # Drop the tables
    User.__table__.drop(op.get_bind())
    UserProfile.__table__.drop(op.get_bind())
    Post.__table__.drop(op.get_bind())
