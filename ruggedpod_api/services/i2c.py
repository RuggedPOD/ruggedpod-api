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

import re

from ruggedpod_api import config
from ruggedpod_api.common import dependency
from ruggedpod_api.services import utils
from ruggedpod_api.services.db import Config, db
from ruggedpod_api.common import exception


class I2CBusDiscovery(object):
    def __init__(self):
        pass

    @staticmethod
    def list_bus():
        rc, stdout, stderr = utils.cmd(i2c['bus_lookup_command'])
        if rc != 0:
            raise exception.NoContent(reason='Cannot find any I2C bus')
        return stdout

    @staticmethod
    def detect(bus):
        rc, stdout, stderr = utils.cmd('i2cdetect -y %s' % bus)
        if rc != 0:
            raise exception.NoContent(reason='Cannot find any I2C bus')
        return stdout


i2c = config.get_attr('i2c')
i2c_discovery = dependency.lookup('i2c_bus_discovery')
ADCHelpers = dependency.lookup('adc_helpers')
ADCPi = dependency.lookup('adc')


def _read_config(session=None):
    if not session:
        session = db.session()
    config = {}
    for c in session.query(Config).filter(Config.category == 'i2c'):
        config[c.key] = c
    return config


def read_power_consumption(blade_id):
    i2cConfig = _read_config()
    try:
        smbus = ADCHelpers().get_smbus(i2cConfig['i2c_power_read_bus'].value)
        adc = ADCPi(smbus, i2cConfig['i2c_power_read_address'].value, None, 12)
        return int((adc.read_raw(i2c['consumption'][blade_id]) * 2 / float(1000) - 2.5) * 10 * 24)
    except:
        return -1


def read_bus():
    i2cConfig = _read_config()
    rawbus = i2c_discovery.list_bus()
    bus = []
    for d in rawbus.split('\n'):
        b = d.strip()
        if b != '':
            id = b.split('-')[1]
            e = {
                'label': b,
                'id': id,
            }
            e['devices'] = []
            if i2cConfig['i2c_power_read_bus'].value == id:
                e['devices'].append({
                    'address': i2cConfig['i2c_power_read_address'].value,
                    'purpose': 'power_read'
                })
            bus.append(e)

    return bus


def read_single_bus(id):
    i2cConfig = _read_config()
    for bus in read_bus():
        if bus['id'] == id:
            return bus
    raise exception.NotFound()


def read_bus_devices(id):
    return read_single_bus(id)['devices']


def detect_bus_devices(id):
    raw = i2c_discovery.detect(id)
    detect = []
    line_count = 0

    for d in raw.split('\n'):
        if line_count == 0:
            line_count = line_count + 1
            continue

        b = d.strip()
        if b != '':
            items = map(str.strip, re.findall('.{1,2} ?', b[4:]))
            while len(items) != 16:
                items.append('')

            detect.append({
                'label': '%02d' % ((line_count - 1) * 10),
                'items': items,
            })
            line_count = line_count + 1

    return detect


def read_single_device(bus_id, address):
    for device in read_single_bus(bus_id)['devices']:
        if device['address'] == address:
            return device
    raise exception.NotFound()


def delete_single_device(bus_id, address):
    for device in read_single_bus(bus_id)['devices']:
        if device['address'] == address:
            session = db.session()
            with session.begin():
                i2cConfig = _read_config(session)
                i2cConfig['i2c_power_read_bus'].value = ''
                i2cConfig['i2c_power_read_address'].value = ''
            return
    raise exception.NotFound()


def setup_device(bus_id, address, data):
    if 'purpose' not in data:
        raise exception.BadRequest(reason="field 'purpose' is missing in request body")

    if data['purpose'] != 'power_read':
        raise exception.BadRequest(reason="Currently, 'purpose' accept only the value 'power_read'")

    read_single_bus(bus_id)  # To ensure this bus id is valid

    session = db.session()
    with session.begin():
        i2cConfig = _read_config(session)
        i2cConfig['i2c_power_read_bus'].value = bus_id
        i2cConfig['i2c_power_read_address'].value = address

    return read_single_device(bus_id, address)
