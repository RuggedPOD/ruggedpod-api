import datetime
import threading

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

from ruggedpod_api import config
from ruggedpod_api.common import ssh
from ruggedpod_api.common.security import hash_password, generate_uuid


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


class ExecCommand(DBObject):
    """
    Describe a command to execute on a blade
    """

    __tablename__ = "commands"

    id = Column(String, primary_key=True)
    blade_id = Column(String)
    status = Column(String)
    submit_date = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    hostname = Column(Integer)
    command = Column(String)
    method = Column(String)
    user = Column(String)
    ssh_private_key = Column(Text)
    std_out = Column(Text)
    std_err = Column(Text)
    status_code = Column(Integer)

    def __init__(self, blade_id, hostname, command, ssh_private_key, user='root', method='ssh'):
        self.id = generate_uuid()
        self.blade_id = blade_id
        self.status = 'PENDING'
        self.hostname = hostname
        self.command = command
        self.method = method
        self.user = user
        self.ssh_private_key = ssh_private_key
        self.submit_date = datetime.datetime.utcnow()

    def _date_iso(self, date):
        if date:
            return date.isoformat()
        return None

    def submit_date_iso(self):
        return self._date_iso(self.submit_date)

    def start_date_iso(self):
        return self._date_iso(self.start_date)

    def end_date_iso(self):
        return self._date_iso(self.end_date)

    def start(self):
        self.start_date = datetime.datetime.utcnow()
        self.status = 'RUNNING'

        cmd_id = self.id
        command = self.command
        hostname = self.hostname
        user = self.user
        ssh_private_key = self.ssh_private_key

        def exec_command():
            status = 'SUCCESS'
            try:
                (rc, stdout_str, stderr_str) = ssh.execute(command, hostname, user, ssh_private_key)
            except:
                status = 'ERROR'

            session = db.session()
            with session.begin():
                c = session.query(ExecCommand).filter(ExecCommand.id == cmd_id).first()
                c.end_date = datetime.datetime.utcnow()
                c.status = status
                c.ssh_private_key = None
                if 'stdout_str' in locals() and stdout_str:
                    c.std_out = stdout_str
                if 'stderr_str' in locals() and stderr_str:
                    c.std_err = stderr_str

        threading.Thread(target=exec_command).start()


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

            if 'i2c_power_read_bus' not in config:
                session.add(Config('i2c', 'i2c_power_read_bus', '1'))

            if 'i2c_power_read_address' not in config:
                session.add(Config('i2c', 'i2c_power_read_address', '0x6c'))


db = Database(base=DBObject)
