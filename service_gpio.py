
import RPi.GPIO as GPIO
from lxml import etree

ledTable={'1' : 7,
          '2' : 12
         }

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    # Set all led in Output
    for led in ledTable:
        GPIO.setup(ledTable[ led ], GPIO.OUT)

def SetBladeAttentionLEDOn( bladeId ):
    GPIO.output( ledTable[ bladeId ], True)
    return 'OK'

def SetBladeAttentionLEDOff( bladeId ):
    GPIO.output( ledTable[ bladeId ], False)
    return 'OK'


