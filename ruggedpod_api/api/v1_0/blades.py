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

from .blueprint import api

from ruggedpod_api.common import exception
from ruggedpod_api.services import gpio_legacy as gpio

from flask import request


@api.route("/SetBladeAttentionLEDOn")
def set_blade_attention_led_on():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.set_blade_attention_led_on(request.args['bladeId'])


@api.route("/SetAllBladesAttentionLEDOn")
def set_all_blades_attention_led_on():
    return gpio.set_all_blades_attention_led_on()


@api.route("/SetBladeAttentionLEDOff")
def set_blade_attention_led_off():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.set_blade_attention_led_off(request.args['bladeId'])


@api.route("/SetAllBladesAttentionLEDOff")
def set_all_blades_attention_led_off():
    return gpio.set_all_blades_attention_led_off()


@api.route("/GetAllPowerConsumption")
def get_all_power_consumption():
    return gpio.get_all_power_consumption()


@api.route("/GetPowerConsumption")
def get_power_consumption():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.get_power_consumption(request.args['bladeId'])


@api.route("/GetAllPowerState")
def get_all_power_state():
    return gpio.get_all_power_state()


@api.route("/GetPowerState")
def get_power_state():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.get_power_state(request.args['bladeId'])


@api.route("/SetPowerOn")
def set_power_on():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.set_power_on(request.args['bladeId'])


@api.route("/SetPowerOff")
def set_power_off():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.set_power_off(request.args['bladeId'])


@api.route("/SetAllPowerOn")
def set_all_power_on():
    return gpio.set_all_power_on()


@api.route("/SetAllPowerOff")
def set_all_power_off():
    return gpio.set_all_power_off()


@api.route("/SetBladeShortOnOff")
def set_blade_short_onoff():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.set_blade_short_onoff(request.args['bladeId'])


@api.route("/SetAllBladesShortOnOff")
def set_all_blades_short_onoff():
    return gpio.set_all_blades_short_onoff()


@api.route("/SetBladeLongOnOff")
def set_blade_long_onoff():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.set_blade_long_onoff(request.args['bladeId'])


@api.route("/SetAllBladesLongOnOff")
def set_all_blades_long_onoff():
    return gpio.set_all_blades_long_onoff()


@api.route("/SetAllBladesReset")
def set_all_blades_reset():
    return gpio.set_all_blades_reset()


@api.route("/StartBladeSerialSession")
def start_blade_serial_session():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.start_blade_serial_session(request.args['bladeId'])


@api.route("/SetBladeReset")
def set_blade_reset():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.set_blade_reset(request.args['bladeId'])


@api.route("/SetBladeOilPumpOn")
def set_blade_oil_pump_on():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.set_blade_oil_pump_on(request.args['bladeId'])


@api.route("/SetAllBladesOilPumpOn")
def set_all_blades_oil_pumps_on():
    return gpio.set_all_blades_oil_pumps_on()


@api.route("/SetBladeOilPumpOff")
def set_blade_oil_pump_off():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.set_blade_oil_pump_off(request.args['bladeId'])


@api.route("/SetAllBladesOilPumpOff")
def set_all_blades_oil_pump_off():
    return gpio.set_all_blades_oil_pump_off()


@api.route("/GetBladeOilPumpStatus")
def get_blade_oil_pump_state():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return gpio.get_blade_oil_pump_state(request.args['bladeId'])


@api.route("/GetAllBladesOilPumpStatus")
def get_all_blades_oil_pump_state():
    return gpio.get_all_blades_oil_pump_state()
