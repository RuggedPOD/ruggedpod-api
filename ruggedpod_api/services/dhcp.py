# RuggedPOD management API
#
# Copyright (C) 2016 Guillaume Giamarchi <guillaume.giamarchi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import subprocess
from jinja2 import Environment, PackageLoader

import ruggedpod_api.common.exception as exception
from ruggedpod_api.services.db import Config, db

tpl = Environment(loader=PackageLoader('ruggedpod_api.services', 'pxe'))


def _exec(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()
    return process.wait()


def read_config(session=None):
    if not session:
        session = db.session()
    config = {}
    for c in session.query(Config).filter(Config.category == 'dhcp'):
        config[c.key] = c.value
    return config


def update_config(config_dict):
    session = db.session()
    with session.begin():
        config = {}
        for c in session.query(Config).filter(Config.category == 'dhcp'):
            config[c.key] = c
        for k in config_dict:
            if k in config:
                config[k].value = config_dict[k]
    refresh()


def refresh():
    config = read_config(db.session())

    with open("/etc/dnsmasq.conf", "w") as text_file:
        text_file.write(tpl.get_template('dnsmasq.conf').render(**config))

    rc = _exec('service dnsmasq restart')

    if (rc != 0):
        raise exception.RuggedpodException()
