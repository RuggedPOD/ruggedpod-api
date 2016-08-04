# RuggedPOD management API
#
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

import mock
from random import randint

GPIO = mock.Mock()

ADCHelpers = mock.Mock()


class ADCPi(object):
    def __init__(self, a, b, c, d):
        pass

    @staticmethod
    def read_raw(n):
        return randint(1370, 1430)


class I2CBusDiscovery(object):
    def __init__(self):
        pass

    @staticmethod
    def list_bus():
        return "i2c-1\ni2c-2\n"
