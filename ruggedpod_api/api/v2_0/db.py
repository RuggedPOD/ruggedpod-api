from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

DBObject = declarative_base()


class User(DBObject):
    """
    Describe a user for the RuggedPOD API
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    login = Column(String)
    pasword = Column(String)
    enabled = Column(Boolean)

    def __init__(self, login, firstname=None, lastname=None, password=None, enabled=True):
        self.login = login
        self.firstname = firstname
        self.lastname = lastname
        self.password = paswaord
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
        self.engine = create_engine('sqlite:////opt/ruggedpod-api/ruggedpod.db', echo=True)  # TODO variabilize

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


db = Database(base=DBObject)
