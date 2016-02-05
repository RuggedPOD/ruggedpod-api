from sqlalchemy.orm.exc import NoResultFound

from ruggedpod_api.services.db import Database, User, db
from ruggedpod_api.common import exception, security


def find(id=None, username=None):
    if id is None and username is None:
        return find_all()

    if id is not None and username is not None:
        raise exception.Conflict()

    if id is not None:
        return findOne(User.id == id)

    if username is not None:
        return findOne(User.username == username)


def findOne(filter):
    session = db.session()
    try:
        with session.begin():
            user = session.query(User).filter(filter).one()
            session.expunge(user)
            return user
    except NoResultFound as e:
        raise exception.NotFound()


def exists(username):
    try:
        find(username=username)
        return True
    except exception.NotFound:
        return False


def find_all():
    session = db.session()
    with session.begin():
        users = session.query(User)
        for user in users:
            session.expunge(user)
        return users


def save(user):
    user.password = security.hash_password(user.password)
    session = db.session()
    with session.begin():
        created_used = session.add(user)
    return user.id


def update(updated_user):
    session = db.session()
    with session.begin():
        user = session.query(User).filter(User.id == updated_user.id).one()
        user.firstname = updated_user.firstname
        user.lastname = updated_user.lastname
        if updated_user.password is not None:
            user.password = security.hash_password(updated_user.password)


def delete(id):
    session = db.session()
    with session.begin():
        user = findOne(User.id == id)
        session.delete(user)
