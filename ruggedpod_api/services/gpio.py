# RuggedPOD management API
#
# Copyright (C) 2015 Maxime Terras <maxime.terras@numergy.com>
# Copyright (C) 2015 Pierre Padrixe <pierre.padrixe@gmail.com>
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

import time

from ruggedpod_api import config
from ruggedpod_api.common import dependency


attention_led_dict = config.get_attr('attention_led')
power_dict = config.get_attr('power')
consumption_dict = config.get_attr('consumption')
reset_dict = config.get_attr('reset')
onoff_dict = config.get_attr('onoff')
short_press = config.get_attr('short_press')
long_press = config.get_attr('long_press')
serial_select_dict = config.get_attr('serial_select')
oil_pump_dict = config.get_attr('oil_pump')
i2c = config.get_attr('i2c')

ADCHelpers = dependency.lookup('adc_helpers')
ADCPi = dependency.lookup('adc')
adc = ADCPi(ADCHelpers().get_smbus(), i2c['dac_power_consumption_addr'], i2c['dac_other_addr'], 12)

GPIO = dependency.lookup('gpio')


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for blade_id in reset_dict:
        GPIO.setup(reset_dict[blade_id], GPIO.OUT)
        GPIO.output(reset_dict[blade_id], True)
    for blade_id in onoff_dict:
        GPIO.setup(onoff_dict[blade_id], GPIO.OUT)
        GPIO.output(onoff_dict[blade_id], False)
    for blade_id in serial_select_dict:
        GPIO.setup(serial_select_dict[blade_id], GPIO.OUT)
        GPIO.output(serial_select_dict[blade_id], False)


def read_power_consumption(blade_id):
    return int((adc.read_raw(consumption_dict[blade_id]) * 2 / float(1000) - 2.5) * 10 * 24)


def set_blade_short_onoff(blade_id):
    GPIO.output(onoff_dict[blade_id], True)
    time.sleep(short_press)
    GPIO.output(onoff_dict[blade_id], False)


def set_all_blades_short_onoff():
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], True)
    time.sleep(short_press)
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], False)


def set_blade_long_onoff(blade_id):
    GPIO.output(onoff_dict[blade_id], True)
    time.sleep(long_press)
    GPIO.output(onoff_dict[blade_id], False)


def set_all_blades_long_onoff():
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], True)
    time.sleep(long_press)
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], False)


def set_blade_reset(blade_id):
    GPIO.output(reset_dict[blade_id], False)
    time.sleep(short_press)
    GPIO.output(reset_dict[blade_id], True)


def set_all_blades_reset():
    for blade_id in reset_dict:
        GPIO.output(reset_dict[blade_id], False)
    time.sleep(short_press)
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], True)


def start_blade_serial_session(blade_id):
    for address_bit in serial_select_dict:
        status = False
        if (((int(blade_id) - 1) >> int(address_bit)) & 1):
            status = True
        GPIO.output(serial_select_dict[address_bit], status)


def set_blade_oil_pump_on(bladeId):
    GPIO.output(oil_pump_dict[bladeId], True)


def set_all_blades_oil_pumps_on():
    for bladeId in oil_pump_dict:
        GPIO.output(oil_pump_dict[bladeId], True)


def set_blade_oil_pump_off(bladeId):
    GPIO.output(oil_pump_dict[bladeId], False)


def set_all_blades_oil_pump_off():
    for bladeId in oil_pump_dict:
        GPIO.output(oil_pump_dict[bladeId], False)
