# RuggedPOD management API
#
# Copyright (C) 2015 Maxime Terras <maxime.terras@numergy.com>
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

import os.path

from ruggedpod_api.common.conf import YmlConf

CONF_FILE = "/etc/ruggedpod/api-conf.yaml"

if not os.path.isfile(CONF_FILE):
    # Get configuration file from project directory
    # This is mainly useful in development mode
    CONF_FILE = "%s/../conf.yaml" % os.path.dirname(os.path.realpath(__file__))

config = YmlConf(CONF_FILE)
