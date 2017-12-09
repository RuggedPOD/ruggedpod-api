# RuggedPOD management API
#
# Copyright (C) 2015 Maxime Terras <maxime.terras@numergy.com>
# Copyright (C) 2015 Pierre Padrixe <pierre.padrixe@gmail.com>
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

from lxml import etree
import time

from ruggedpod_api import config
from ruggedpod_api.common import dependency


reset_dict = config.get_attr('reset')
onoff_dict = config.get_attr('onoff')
short_press = config.get_attr('short_press')
long_press = config.get_attr('long_press')
serial_select_dict = config.get_attr('serial_select')
oil_pump_dict = config.get_attr('oil_pump')
i2c = config.get_attr('i2c')
consumption_dict = i2c['consumption']

ADCHelpers = dependency.lookup('adc_helpers')
ADCPi = dependency.lookup('adc')

GPIO = dependency.lookup('gpio')


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for blade_id in reset_dict:
        GPIO.setup(reset_dict[blade_id], GPIO.OUT)
    for blade_id in onoff_dict:
        GPIO.setup(onoff_dict[blade_id], GPIO.OUT)
    for blade_id in serial_select_dict:
        GPIO.setup(serial_select_dict[blade_id], GPIO.OUT)
        GPIO.output(serial_select_dict[blade_id], False)


def _set_default_xml_attr(response):
    etree.SubElement(response, 'CompletionCode').text = 'Success'
    etree.SubElement(response, 'statusDescription').text = ''
    etree.SubElement(response, 'apiVersion').text = '1'


def get_all_power_consumption():
    response = etree.Element('GetAllPowerConsumptionResponse')
    for blade_id in consumption_dict:
        consumption = etree.SubElement(response, 'PowerConsumptionResponse')
        blade = etree.SubElement(consumption, 'bladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = blade_id
        value = read_power_consumption(blade_id)
        etree.SubElement(consumption, 'powerConsumption').text = str(value)
    return etree.tostring(response, pretty_print=True)


def get_power_consumption(blade_id):
    response = etree.Element('PowerConsumptionResponse')
    blade = etree.SubElement(response, 'bladeResponse')
    _set_default_xml_attr(blade)
    etree.SubElement(blade, 'bladeNumber').text = blade_id
    value = read_power_consumption(blade_id)
    etree.SubElement(response, 'powerConsumption').text = str(value)
    return etree.tostring(response, pretty_print=True)


def read_power_consumption(blade_id):
    try:
        adc = ADCPi(ADCHelpers().get_smbus(i2c['bus']), i2c['dac_power_consumption_addr'], None, 12)
        return int((adc.read_raw(consumption_dict[blade_id]) * 2 / float(1000) - 2.5) * 10 * 24)
    except:
        traceback.print_exc()
        return -1


def get_all_power_state():
    response = etree.Element('GetAllPowerStateResponse')
    for blade_id in power_dict:
        if GPIO.input(power_dict[blade_id]):
            PowerState = 'ON'
        else:
            PowerState = 'OFF'
        power = etree.SubElement(response, 'PowerStateResponse')
        blade = etree.SubElement(power, 'bladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = blade_id
        etree.SubElement(power, 'powerState').text = PowerState
    return etree.tostring(response, pretty_print=True)


def get_power_state(blade_id):
    print 'OK'
    response = etree.Element('PowerStateResponse')
    if GPIO.input(power_dict[blade_id]):
        PowerState = 'ON'
    else:
        PowerState = 'OFF'
    blade = etree.SubElement(response, 'bladeResponse')
    _set_default_xml_attr(blade)
    etree.SubElement(blade, 'bladeNumber').text = blade_id
    etree.SubElement(response, 'powerState').text = PowerState
    return etree.tostring(response, pretty_print=True)


def set_power_on(blade_id):
    GPIO.output(power_dict[blade_id], True)
    response = etree.Element('BladeResponse')
    _set_default_xml_attr(response)
    etree.SubElement(response, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_power_off(blade_id):
    GPIO.output(power_dict[blade_id], False)
    response = etree.Element('BladeResponse')
    _set_default_xml_attr(response)
    etree.SubElement(response, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_all_power_on():
    response = etree.Element('AllBladesResponse')
    for blade_id in power_dict:
        GPIO.output(power_dict[blade_id], True)
        blade = etree.SubElement(response, 'BladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_all_power_off():
    response = etree.Element('AllBladesResponse')
    for blade_id in power_dict:
        GPIO.output(power_dict[blade_id], False)
        blade = etree.SubElement(response, 'BladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_blade_short_onoff(blade_id):
    GPIO.output(onoff_dict[blade_id], True)
    time.sleep(short_press)
    GPIO.output(onoff_dict[blade_id], False)
    response = etree.Element('BladeResponse')
    _set_default_xml_attr(response)
    etree.SubElement(response, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_all_blades_short_onoff():
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], True)
    time.sleep(short_press)
    response = etree.Element('AllBladesResponse')
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], False)
        blade = etree.SubElement(response, 'BladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_blade_long_onoff(blade_id):
    GPIO.output(onoff_dict[blade_id], True)
    time.sleep(long_press)
    GPIO.output(onoff_dict[blade_id], False)
    response = etree.Element('BladeResponse')
    _set_default_xml_attr(response)
    etree.SubElement(response, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_all_blades_long_onoff():
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], True)
    time.sleep(long_press)
    response = etree.Element('AllBladesResponse')
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], False)
        blade = etree.SubElement(response, 'BladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_blade_reset(blade_id):
    GPIO.output(reset_dict[blade_id], False)
    time.sleep(short_press)
    GPIO.output(reset_dict[blade_id], True)
    response = etree.Element('BladeResponse')
    _set_default_xml_attr(response)
    etree.SubElement(response, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_all_blades_reset():
    for blade_id in reset_dict:
        GPIO.output(reset_dict[blade_id], False)
    time.sleep(short_press)
    response = etree.Element('AllBladesResponse')
    for blade_id in onoff_dict:
        GPIO.output(onoff_dict[blade_id], True)
        blade = etree.SubElement(response, 'BladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def start_blade_serial_session(blade_id):
    for address_bit in serial_select_dict:
        status = False
        if (((int(blade_id) - 1) >> int(address_bit)) & 1):
            status = True
        GPIO.output(serial_select_dict[address_bit], status)
    response = etree.Element('BladeResponse')
    _set_default_xml_attr(response)
    etree.SubElement(response, 'bladeNumber').text = blade_id
    return etree.tostring(response, pretty_print=True)


def set_blade_oil_pump_on(bladeId):
    GPIO.output(oil_pump_dict[bladeId], True)
    response = etree.Element('BladeResponse')
    _set_default_xml_attr(response)
    etree.SubElement(response, 'bladeNumber').text = bladeId
    return etree.tostring(response, pretty_print=True)


def set_all_blades_oil_pumps_on():
    response = etree.Element('AllBladesResponse')
    for bladeId in oil_pump_dict:
        GPIO.output(oil_pump_dict[bladeId], True)
        blade = etree.SubElement(response, 'BladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = bladeId
    return etree.tostring(response, pretty_print=True)


def set_blade_oil_pump_off(bladeId):
    GPIO.output(oil_pump_dict[bladeId], False)
    response = etree.Element('BladeResponse')
    _set_default_xml_attr(response)
    etree.SubElement(response, 'bladeNumber').text = bladeId
    return etree.tostring(response, pretty_print=True)


def set_all_blades_oil_pump_off():
    response = etree.Element('AllBladesResponse')
    for bladeId in oil_pump_dict:
        GPIO.output(oil_pump_dict[bladeId], False)
        blade = etree.SubElement(response, 'BladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = bladeId
    return etree.tostring(response, pretty_print=True)


def get_all_blades_oil_pump_state():
    response = etree.Element('GetAllOilPumpStateResponse')
    for bladeId in PowerTable:
        if GPIO.input(oil_pump_dict[bladeId]):
            oil_pump_state = 'ON'
        else:
            oil_pump_state = 'OFF'
        power = etree.SubElement(response, 'OilPumpStateResponse')
        blade = etree.SubElement(power, 'bladeResponse')
        _set_default_xml_attr(blade)
        etree.SubElement(blade, 'bladeNumber').text = bladeId
        etree.SubElement(power, 'powerState').text = oil_pump_state
    return etree.tostring(response, pretty_print=True)


def get_blade_oil_pump_state(bladeId):
    response = etree.Element('OilPumpStateResponse')
    if GPIO.input(oil_pump_dict[bladeId]):
        oil_pump_state = 'ON'
    else:
        oil_pump_state = 'OFF'
    blade = etree.SubElement(response, 'bladeResponse')
    etree.SubElement(blade, 'CompletionCode').text = 'Success'
    etree.SubElement(blade, 'statusDescription').text = ''
    etree.SubElement(blade, 'apiVersion').text = '1'
    etree.SubElement(blade, 'bladeNumber').text = bladeId
    etree.SubElement(response, 'powerState').text = OilPumpState
    return etree.tostring(response, pretty_print=True)
