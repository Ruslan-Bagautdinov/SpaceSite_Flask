from werkzeug.security import generate_password_hash

from database.models import db, User, UserProfile


def get_user_by_username(username: str):
    user = User.query.filter_by(username=username).first()
    return user


def get_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    return user


def get_user_profile(user_id: int):
    user_profile = UserProfile.query.filter_by(id=user_id).one()
    return user_profile


def create_new_user(username, email, password):

    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    new_user_profile = UserProfile(
        user_id=new_user.id,
        first_name=None,
        last_name=None,
        phone_number=None,
        photo=None,
        user_age=None
    )
    db.session.add(new_user_profile)
    db.session.commit()


def delete_user(user_id: int):

    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
