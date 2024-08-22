from datetime import datetime

from werkzeug.security import generate_password_hash

from database.models import db, User, UserProfile, Post


def get_all_users():
    return User.query.all()


def get_user_by_username(username: str):
    user = User.query.filter_by(username=username).first()
    return user


def get_user_by_email(email: str):
    user = User.query.filter_by(email=email).first()
    return user


def new_user_check(username: str, email: str):
    user = User.query.filter((User.username == username) | (User.email == email)).first()
    if user:
        if user.username == username:
            return "username"
        if user.email == email:
            return "email"
    return None


def get_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    return user


def get_user_profile(user_id: int):
    user_profile = UserProfile.query.filter_by(user_id=user_id).one()
    return user_profile


def create_new_user(username, email, password, role='user'):
    password_hash = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=password_hash, role=role)
    db.session.add(new_user)
    db.session.commit()

    new_user_profile = UserProfile(
        user_id=new_user.id,
        first_name=None,
        last_name=None,
        phone_number=None,
        user_photo=None,
        user_age=None
    )
    db.session.add(new_user_profile)
    db.session.commit()


def update_user_profile(user_id: int,
                        first_name: str | None,
                        last_name: str | None,
                        phone_number: str | None,
                        user_photo: str | None,
                        user_age: int | None):
    user_profile = get_user_profile(user_id)

    if user_profile:
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.phone_number = phone_number
        user_profile.user_photo = user_photo
        user_profile.user_age = user_age
        db.session.commit()
        return True
    return False


def update_user_role(user_id: int, role: str):
    user = get_user(user_id)
    if user:
        user.role = role
        db.session.commit()
        return True
    return False


def delete_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False


def create_post(user_id, content):
    new_post = Post(content=content, user_id=user_id, created_at=datetime.utcnow())
    db.session.add(new_post)
    db.session.commit()
    return new_post


def get_post(post_id):
    return Post.query.get(post_id)


def update_post(post_id, content=None):
    post = get_post(post_id)
    if post:
        if content:
            post.content = content
        db.session.commit()
        return True
    return False


def delete_post(post_id):
    post = get_post(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return True
    return False


def get_all_posts():
    return Post.query.all()


def get_user_posts(user_id, page=1, per_page=15, count=False):
    if count:
        return Post.query.filter_by(user_id=user_id).count()
    else:
        return Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).paginate(page=page,
                                                                                               per_page=per_page,
                                                                                               error_out=False).items



