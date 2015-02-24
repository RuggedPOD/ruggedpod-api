from flask import Flask, request
import RPi.GPIO as GPIO
from lxml import etree


app = Flask(__name__)


# 
ledTable={'1' : 7,
          '2' : 12
         }


@app.route("/SetBladeAttentionLEDOn")
def SetBladeAttentionLEDOn():
    if 'bladeId' in request.args:
        GPIO.output(ledTable[request.args['bladeId']], True)
        return 'OK'
    else:
        return 'Set bladeId'


@app.route("/SetBladeAttentionLEDOff")
def SetBladeAttentionLEDOff():
    if 'bladeId' in request.args:
        GPIO.output(ledTable[request.args['bladeId']], False)
        return 'OK'
    else:
        return 'Set bladeId'

@app.route("/SetAllBladesAttentionLEDOn")
def SetAllBladesAttentionLEDOn():
    for led in ledTable:
        GPIO.output(ledTable[ led ], True)
    return 'OK'

@app.route("/SetAllBladesAttentionLEDOff")
def SetAllBladesAttentionLEDOff():
    for led in ledTable:
        GPIO.output(ledTable[ led ], False)
    return 'OK'


if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Set all led in Output
    for led in ledTable:
        GPIO.setup(ledTable[ led ], GPIO.OUT)

    app.run(host= '0.0.0.0')
    app.run()
