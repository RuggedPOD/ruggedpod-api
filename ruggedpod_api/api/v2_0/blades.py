# RuggedPOD management API
#
# Copyright (C) 2015 Maxime Terras <maxime.terras@numergy.com>
# Copyright (C) 2015 Guillaume Giamarchi <guillaume.giamarchi@gmail.com>
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

import json
import shutil
import os
import re
import socket
import fcntl
import struct

from .blueprint import api

from ruggedpod_api.api import utils
from ruggedpod_api.common import exception
from ruggedpod_api.services import gpio, i2c, dhcp, network
from ruggedpod_api.services.db import Database, Blade, db

from flask import request
from jinja2 import Environment, PackageLoader

tpl = Environment(loader=PackageLoader('ruggedpod_api.services', 'pxe'))


@api.route("/blades", methods=['GET'])
def get_blades():
    session = db.session()
    with session.begin():
        blades = []
        for b in session.query(Blade):
            mac_address = network.format_mac_address_standard(b.mac_address)
            blades.append({
                'id': b.id,
                'name': b.name,
                'description': b.description,
                'building': b.building,
                'mac_address': mac_address,
                'ip_address': network.read_ip_address(mac_address),
                'consumption': i2c.read_power_consumption(str(b.id))
            })
        return json.dumps(blades)


@api.route("/blades/reset", methods=['PATCH'])
def reset_blades():
    gpio.set_all_blades_reset()
    return "", 204


@api.route("/blades/power", methods=['PATCH'])
def power_blades():
    if _long_action():
        gpio.set_all_blades_long_onoff()
    else:
        gpio.set_all_blades_short_onoff()
    return "", 204


@api.route("/blades/<id>", methods=['GET'])
def get_blade(id):
    session = db.session()
    with session.begin():
        blade = _get_blade(id, session)
        mac_address = network.format_mac_address_standard(blade.mac_address)
        return json.dumps({
            'id': blade.id,
            'name': blade.name,
            'description': blade.description,
            'building': blade.building,
            'mac_address': mac_address,
            'ip_address': network.read_ip_address(mac_address),
            'consumption': i2c.read_power_consumption(str(blade.id))
        })


@api.route("/blades/<id>", methods=['PUT'])
def update_blade(id):
    session = db.session()
    with session.begin():
        blade = _get_blade(id, session)

        data = utils.parse_json_body(request)
        if 'id' in data and int(data['id']) != int(id):
            raise exception.Conflict(reason="Id mismatch")

        if 'name' in data:
            blade.name = data['name']

        if 'description' in data:
            blade.description = data['description']

        if 'mac_address' in data:
            blade.mac_address = network.normalize_mac_address(data['mac_address'])

    return get_blade(id)


@api.route("/blades/<id>/reset", methods=['PATCH'])
def reset_blade(id):
    _get_blade(id, db.session())
    gpio.set_blade_reset(id)
    return "", 204


@api.route("/blades/<id>/power", methods=['PATCH'])
def power_blade(id):
    _get_blade(id, db.session())
    if _long_action():
        gpio.set_blade_long_onoff(id)
    else:
        gpio.set_blade_short_onoff(id)
    return "", 204


@api.route("/blades/<id>/serial", methods=['PATCH'])
def serial_blade(id):
    _get_blade(id, db.session())
    gpio.start_blade_serial_session(id)
    return "", 204


def _write_template(template, dstfile, model):
    with open(dstfile, "w") as text_file:
        text_file.write(tpl.get_template(template).render(**model))


def _get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


@api.route("/blades/<id>/build", methods=['POST'])
def build_blade(id):
    session = db.session()
    with session.begin():
        blade = _get_blade(id, session)
        if blade.building:
            raise exception.Conflict(reason="A building operation is already in progress")
        if not blade.mac_address:
            raise exception.Conflict(reason="Blade must have is MAC address set in order to be built")

        pxe_tftp_dir = "/tftp/pxe/pxelinux.cfg"
        pwe_www_dir = "/var/www/pxe"
        pxe_mac_address = network.format_mac_address_pxe(blade.mac_address)

        ip = _get_ip_address('eth0')

        # Default values
        os = 'ubuntu1404'
        hostname = 'blade' + str(blade.id)
        username = 'ruggedpod'
        ssh_pub_key = ''
        password = ''

        data = utils.parse_json_body(request)

        if 'os' in data and data['os']:
            os = data['os']

        if 'username' in data and data['username']:
            username = data['username']

        if 'hostname' in data and data['hostname']:
            hostname = data['hostname']

        if 'ssh_pub_key' not in data or not data['ssh_pub_key']:
            if 'password' not in data:
                raise exception.BadRequest(
                        reason="A password or a SSH public key must be provided for user '%s'" % username)

            if not data['password']:
                raise exception.BadRequest(
                        reason="A password or a SSH public key must be provided for user '%s'" % username)

            password = data['password']
        else:
            ssh_pub_key = data['ssh_pub_key']
            if 'password' in data and data['password']:
                password = data['password']

        _write_template("ubuntu-1404/pxemenu", "%s/%s" % (pxe_tftp_dir, pxe_mac_address), {
            'pxe_server': ip,
            'preseed_filename': "%s.seed" % pxe_mac_address,
            'serial_baudrate': 115200
        })

        _write_template("ubuntu-1404/preseed", "%s/%s.seed" % (pwe_www_dir, pxe_mac_address), {
            'http_proxy': "http://%s:3128" % ip,
            'ubuntu_mirror': "archive.ubuntu.com",
            'root_password': "todo",
            'ntp_server_host': ip,
            'pxe_server': ip,
            'post_install_script_name': "%s.sh" % pxe_mac_address
        })

        post_install_model = {
            'blade_number': blade.id,
            'serial_baudrate': 115200,
            'api_base_url': "http://%s:5000" % ip,
            'username': username,
            'hostname': hostname
        }

        if password:
            post_install_model['password'] = password

        if ssh_pub_key:
            post_install_model['ssh_pub_key'] = ssh_pub_key

        _write_template("ubuntu-1404/post-install.sh", "%s/%s.sh" % (pwe_www_dir, pxe_mac_address),
                        post_install_model)

        blade.building = True

    return "", 204


@api.route("/blades/<id>/build", methods=['DELETE'])
def cancel_build_blade(id):
    session = db.session()
    with session.begin():
        blade = _get_blade(id, session)
        if not blade.building:
            raise exception.Conflict(reason="The server is not in the building state")

        pxe_tftp_dir = "/tftp/pxe/pxelinux.cfg"
        pwe_www_dir = "/var/www/pxe"
        pxe_mac_address = network.format_mac_address_pxe(blade.mac_address)

        os.remove("%s/%s" % (pxe_tftp_dir, pxe_mac_address))
        os.remove("%s/%s.seed" % (pwe_www_dir, pxe_mac_address))
        os.remove("%s/%s.sh" % (pwe_www_dir, pxe_mac_address))

        blade.building = False

    return "", 204


def _get_blade(id, session):
    blade = session.query(Blade).filter(Blade.id == id).first()
    if blade is None:
        raise exception.NotFound()
    return blade


def _long_action():
    long = request.args.get('long')
    return long is not None and (long.lower() == 'true' or long == '')
