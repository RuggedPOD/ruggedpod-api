
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
        return service.SetBladeAttentionLEDOn( request.args['bladeId'] )
    else:
        return 'Set bladeId'

@app.route("/SetAllBladesAttentionLEDOn")
def SetAllBladesAttentionLEDOn():
    return service.SetAllBladesAttentionLEDOn()

@app.route("/SetBladeAttentionLEDOff")
def SetBladeAttentionLEDOff():
    if 'bladeId' in request.args:
        return service.SetBladeAttentionLEDOff( request.args['bladeId'] )
    else:
        return 'Set bladeId'

@app.route("/SetAllBladesAttentionLEDOff")
def SetAllBladesAttentionLEDOff():
    return service.SetAllBladesAttentionLEDOff()



if __name__ == "__main__":
    service.init()

    app.run(host= '0.0.0.0')
    app.run()
