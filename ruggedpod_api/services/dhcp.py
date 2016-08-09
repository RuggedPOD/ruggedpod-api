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
from netaddr import IPNetwork, IPAddress
from netaddr.core import AddrFormatError

from ruggedpod_api.common import exception
from ruggedpod_api.services import utils
from ruggedpod_api.services.db import Config, db

tpl = Environment(loader=PackageLoader('ruggedpod_api.services', 'pxe'))


def read_config(session=None):
    if not session:
        session = db.session()
    config = {}
    for c in session.query(Config).filter(Config.category == 'dhcp'):
        config[c.key] = c.value
    return config


def _normalize_cidr(raw_cidr):
    try:
        network = IPNetwork(raw_cidr)
        cidr = str(network)
    except AddrFormatError:
        raise exception.Conflict(reason="Invalid network address format")

    if not network.is_private():
        raise exception.Conflict(reason="Invalid network address. Must be RFC1918 compliant")

    return cidr


def update_config(config_dict):
    session = db.session()
    with session.begin():
        config = {}
        for c in session.query(Config).filter(Config.category == 'dhcp'):
            config[c.key] = c
        for k in config_dict:
            if k in config:
                config[k].value = config_dict[k]

        if config['dhcp_mode'].value not in ['proxy', 'dhcp']:
            raise exception.Conflict(reason="Invalid DHCP mode. Must be either 'proxy' or 'dhcp'")

        config['dhcp_network'].value = _normalize_cidr(config['dhcp_network'].value)

        if config['dhcp_mode'].value == 'dhcp':
            try:
                start = int(IPAddress(config['dhcp_range_start'].value))
            except AddrFormatError:
                raise exception.Conflict(reason="Invalid format for DHCP start range IP address")
            try:
                end = int(IPAddress(config['dhcp_range_end'].value))
            except AddrFormatError:
                raise exception.Conflict(reason="Invalid format for DHCP end range IP address")

            network = IPNetwork(config['dhcp_network'].value)
            network_ip = int(network.ip)
            netmask = int(network.netmask)
            network_checksum = network_ip & netmask

            start_checksum = start & netmask
            if start_checksum != network_checksum:
                raise exception.Conflict(
                        reason="Invalid DHCP start range IP address. Must be in network %s" % str(network))

            end_checksum = end & netmask
            if end_checksum != network_checksum:
                raise exception.Conflict(
                        reason="Invalid DHCP end range IP address. Must be in network %s" % str(network))

            if start > end:
                raise exception.Conflict(reason="DHCP end range must be greater than start range")

            if config['dhcp_lease_duration'].value != 'infinite':
                try:
                    time = int(config['dhcp_lease_duration'].value)
                    if time < 300:
                        raise exception.Conflict(reason="DHCP lease duration must be at least 300 seconds")
                except ValueError:
                    raise exception.Conflict(
                            reason="DHCP lease duration must be either a count in seconds or the word 'infinite'")

    refresh()


def refresh():
    config = read_config(db.session())

    network = IPNetwork(config['dhcp_network'])
    config['dhcp_range_netmask'] = str(network.netmask)

    if config['dhcp_mode'] == 'proxy':
        config['dhcp_range_start'] = str(IPAddress(int(network.ip) + 1))

    with open("/etc/dnsmasq.conf", "w") as text_file:
        text_file.write(tpl.get_template('dnsmasq.conf').render(**config))

    rc, stdout, stderr = utils.cmd('service dnsmasq restart')

    if (rc != 0):
        raise exception.RuggedpodException()
