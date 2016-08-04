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
    username = Column(String(20), nullable=False, unique=True)
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
    mac_address = Column(String)
    ip_address = Column(String)
    building = Column(Boolean, nullable=False)

    def __init__(self, id, name=None, description=None, enabled=True):
        self.id = id
        self.name = name
        self.description = description
        self.enabled = enabled
        self.building = False


class Config(DBObject):
    """
    Describe a generic configuration entry
    """

    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    key = Column(String, nullable=False, unique=True)
    value = Column(String)

    def __init__(self, category, key, value):
        self.category = category
        self.key = key
        self.value = value


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
                user = User(firstname='Administrator', username='admin', password=hash_password('admin'))
                session.add(user)

            config = {}
            for c in session.query(Config):
                config[c.key] = c

            if 'dhcp_mode' not in config:
                session.add(Config('dhcp', 'dhcp_mode', 'proxy'))

            if 'dhcp_network' not in config:
                session.add(Config('dhcp', 'dhcp_network', None))

            if 'dhcp_range_start' not in config:
                session.add(Config('dhcp', 'dhcp_range_start', None))

            if 'dhcp_range_end' not in config:
                session.add(Config('dhcp', 'dhcp_range_end', None))

            if 'dhcp_lease_duration' not in config:
                session.add(Config('dhcp', 'dhcp_lease_duration', 'infinite'))


db = Database(base=DBObject)
