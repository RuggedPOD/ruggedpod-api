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

from ruggedpod_api import config
from ruggedpod_api.common import dependency


i2c = config.get_attr('i2c')
ADCHelpers = dependency.lookup('adc_helpers')
ADCPi = dependency.lookup('adc')


def read_power_consumption(blade_id):
    try:
        adc = ADCPi(ADCHelpers().get_smbus(i2c['bus']), i2c['dac_power_consumption_addr'], None, 12)
        return int((adc.read_raw(i2c['consumption'][blade_id]) * 2 / float(1000) - 2.5) * 10 * 24)
    except:
        return -1
