import sys
from flask import Flask, request

from common import exception
import service_gpio as service


app = Flask(__name__)


@app.route("/SetBladeAttentionLEDOn")
def set_blade_attention_led_on():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.set_blade_attention_led_on(request.args['bladeId'])


@app.route("/SetAllBladesAttentionLEDOn")
def set_all_blades_attention_led_on():
    return service.set_all_blades_attention_led_on()


@app.route("/SetBladeAttentionLEDOff")
def set_blade_attention_led_off():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.set_blade_attention_led_off(request.args['bladeId'])


@app.route("/SetAllBladesAttentionLEDOff")
def set_all_blades_attention_led_off():
    return service.set_all_blades_attention_led_off()


@app.route("/GetAllPowerState")
def get_all_power_state():
    return service.get_all_power_state()


@app.route("/GetPowerState")
def get_power_state():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.get_power_state(request.args['bladeId'])


@app.route("/SetPowerOn")
def set_power_on():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.set_power_on(request.args['bladeId'])


@app.route("/SetPowerOff")
def set_power_off():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.set_power_off(request.args['bladeId'])


@app.route("/SetAllPowerOn")
def set_all_power_on():
    return service.set_all_power_on()


@app.route("/SetAllPowerOff")
def set_all_power_off():
    return service.set_all_power_off()


@app.route("/SetBladeShortOnOff")
def set_blade_short_onoff():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.set_blade_short_onoff(request.args['bladeId'])


@app.route("/SetAllBladesShortOnOff")
def set_all_blades_short_onoff():
    return service.set_all_blades_short_onoff()


@app.route("/SetBladeLongOnOff")
def set_blade_long_onoff():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.set_blade_long_onoff(request.args['bladeId'])


@app.route("/SetAllBladesLongOnOff")
def set_all_blades_long_onoff():
    return service.set_all_blades_long_onoff()


@app.route("/SetBladeReset")
def set_blade_reset():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.set_blade_reset(request.args['bladeId'])


@app.route("/SetAllBladesReset")
def set_all_blades_reset():
    return service.set_all_blades_reset()


@app.route("/StartBladeSerialSession")
def start_blade_serial_session():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.start_blade_serial_session(request.args['bladeId'])


@app.errorhandler(exception.ParameterMissing)
def attribute_missing_handler(error):
    return error.message, error.status_code


@app.route("/SetBladeOilPumpOn")
def set_blade_oil_pump_on():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.set_blade_oil_pump_on(request.args['bladeId'])


@app.route("/SetAllBladesOilPumpOn")
def set_all_blades_oil_pumps_on():
    return service.set_all_blades_oil_pumps_on()


@app.route("/SetBladeOilPumpOff")
def set_blade_oil_pump_off():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.set_blade_oil_pump_off(request.args['bladeId'])


@app.route("/SetAllBladesOilPumpOff")
def set_all_blades_oil_pump_off():
    return service.set_all_blades_oil_pump_off()


@app.route("/GetBladeOilPumpStatus")
def get_blade_oil_pump_state():
    if 'bladeId' not in request.args:
        raise exception.ParameterMissing(name="bladeId")
    return service.get_blade_oil_pump_state(request.args['bladeId'])


@app.route("/GetAllBladesOilPumpStatus")
def get_all_blades_oil_pump_state():
    return service.get_all_blades_oil_pump_state()


if __name__ == "__main__":
    service.init()

    if '--debug' in sys.argv:
        app.debug = True
    app.run(host='0.0.0.0')
