from ruggedpod_api.services.db import Database, User, db

from sqlalchemy.orm.exc import NoResultFound


def find(username):
    session = db.session()
    try:
        with session.begin():
            user = session.query(User).filter(User.login == username).one()
            session.expunge(user)
            return user
    except NoResultFound as e:
        raise exception.NotFound()
