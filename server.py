
import sys
from flask import Flask, request
app = Flask(__name__)

if '-m' in sys.argv:
    mock = 1
else:
    mock = 0


if mock == 1:
    import service_mock as service
else:
    import service_gpio as service


@app.route("/SetBladeAttentionLEDOn")
def SetBladeAttentionLEDOn():
    if 'bladeId' in request.args:
        return service.SetBladeAttentionLEDOn(request.args['bladeId'])
    else:
        return 'Set bladeId'

@app.route("/SetAllBladesAttentionLEDOn")
def SetAllBladesAttentionLEDOn():
    return service.SetAllBladesAttentionLEDOn()

@app.route("/SetBladeAttentionLEDOff")
def SetBladeAttentionLEDOff():
    if 'bladeId' in request.args:
        return service.SetBladeAttentionLEDOff(request.args['bladeId'])
    else:
        return 'Set bladeId'

@app.route("/SetAllBladesAttentionLEDOff")
def SetAllBladesAttentionLEDOff():
    return service.SetAllBladesAttentionLEDOff()

@app.route("/GetAllPowerState")
def GetAllPowerState():
    return service.GetAllPowerState()

@app.route("/GetPowerState")
def GetPowerState():
    if 'bladeId' in request.args:
        return service.GetPowerState(request.args['bladeId'])
    else:
        return 'Set bladeId'

@app.route("/SetPowerOn")
def SetPowerOn():
    if 'bladeId' in request.args:
        return service.SetPowerOn(request.args['bladeId'])
    else:
        return 'Set bladeId'

@app.route("/SetPowerOff")
def SetPowerOff():
    if 'bladeId' in request.args:
        return service.SetPowerOff(request.args['bladeId'])
    else:
        return 'Set bladeId'

@app.route("/SetAllPowerOn")
def SetAllPowerOn():
    return service.SetAllPowerOn()

@app.route("/SetAllPowerOff")
def SetAllPowerOff():
    return service.SetAllPowerOff()

@app.route("/SetBladeShortOnOff")
def SetBladeShortOnOff():
    if 'bladeId' in request.args:
        return service.SetBladeShortOnOff(request.args['bladeId'])
    else:
        return 'Set bladeId'

@app.route("/SetAllBladesShortOnOff")
def SetAllBladesShortOnOff():
    return service.SetAllBladesShortOnOff()

@app.route("/SetBladeLongOnOff")
def SetBladeLongOnOff():
    if 'bladeId' in request.args:
        return service.SetBladeLongOnOff(request.args['bladeId'])
    else:
        return 'Set bladeId'

@app.route("/SetAllBladesLongOnOff")
def SetAllBladesLongOnOff():
    return service.SetAllBladesLongOnOff()

@app.route("/StartBladeSerialSession")
def StartBladeSerialSession():
    if 'bladeId' in request.args:
        return service.StartBladeSerialSession(request.args['bladeId'])
    else:
        return 'Set bladeId'


if __name__ == "__main__":
    service.init()

    app.run(host= '0.0.0.0')
