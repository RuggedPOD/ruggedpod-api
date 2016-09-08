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

from ruggedpod_api.common import exception
from ruggedpod_api.services import dhcp, utils

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))


def normalize_mac_address(mac):
    return mac.encode("ascii").translate(None, ":- ").lower()


def format_mac_address_standard(mac):
    if not mac:
        return None
    n = normalize_mac_address(mac)
    return ':'.join(n[i:i+2] for i in range(0, 12, 2))


def format_mac_address_pxe(mac):
    n = normalize_mac_address(mac)
    return "01-%s" % '-'.join(n[i:i+2] for i in range(0, 12, 2))


def read_ip_address(mac):
    if not mac:
        return None

    dhcp_config = dhcp.read_config()

    if dhcp_config['dhcp_mode'] == 'dhcp':
        return dhcp.read_ip_address_from_lease(mac)

    ip = _read_ip_address_from_arp_table(mac)

    if ip:
        return ip

    _network_discovery(dhcp_config['dhcp_network'])

    return _read_ip_address_from_arp_table(mac)


@cache.cache('_network_discovery', expire=120)
def _network_discovery(net_cidr):
    nmap_cmd = "nmap --min-hostgroup 256 --min-parallelism 256 -sn %s" % net_cidr
    rc, stdout, stderr = utils.cmd(nmap_cmd)
    if rc != 0:
        raise exception.RuggedpodException()


def _read_ip_address_from_arp_table(mac):
    rc, stdout, stderr = utils.cmd("arp -an")

    if rc != 0:
        raise exception.RuggedpodException()

    n_mac = format_mac_address_standard(mac)

    for line in stdout.split('\n'):
        search = re.search('.* \(([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\) .* ([0-9a-f:]{17}) .*', line)
        if search and n_mac == search.group(2):
            return search.group(1)

    return None
