from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

from ruggedpod_api import config
from ruggedpod_api.common.security import hash_password

storage = config.get_attr('storage')

DBObject = declarative_base()


class User(DBObject):
    """
    Describe a user for the RuggedPOD API
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String)
    password = Column(String)
    enabled = Column(Boolean)

    def __init__(self, username=None, firstname=None, lastname=None, password=None, enabled=True):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.enabled = enabled


class Blade(DBObject):
    """
    Describe a blade in the RuggedPOD
    """

    __tablename__ = "blades"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    enabled = Column(Boolean)

    def __init__(self, id, name=None, description=None, enabled=True):
        self.id = id
        self.name = name
        self.description = description
        self.enabled = enabled


class Database(object):
    """
    The Database object is used to manage database sessions
    """

    def __init__(self, base):
        self.base = base
        self.engine = create_engine("sqlite:///%s" % storage['file'], echo=True)  # TODO variabilize

    def session(self):
        Session = sessionmaker(bind=self.engine, autocommit=True)
        return Session()

    def init(self):
        self.base.metadata.create_all(self.engine)
        session = self.session()
        with session.begin():
            blades = {}
            for b in session.query(Blade):
                blades[b.id] = b

            for i in range(1, 5):
                if i not in blades:
                    blade = Blade(i)
                    session.add(blade)

            if session.query(User).filter(User.username == 'admin').count() == 0:
                user = User(username='admin', password=hash_password('admin'))
                session.add(user)


db = Database(base=DBObject)
