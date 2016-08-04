#!/usr/bin/python
try:
    import smbus
except ImportError:
    raise ImportError("python-smbus not found. Install with 'sudo apt-get install python-smbus'")
import re

from ruggedpod_api import config

"""
================================================
ABElectronics Python Helper Functions
Version 1.1 Created 20/01/2015
Python 2 only
Requires python 2 smbus to be installed with: sudo apt-get install python-smbus
This file contains functions to load puthon smbus into an instance variable.
The bus object can then be used by multiple devices without conflicts.
================================================
"""

class ABEHelpers:

    def get_smbus(self, bus):
        try:
            return smbus.SMBus(bus)
        except IOError:
                print ("Could not open the i2c bus.")
                print ("Please check that i2c is enabled and python-smbus and i2c-tools are installed.")
                print ("Visit https://www.abelectronics.co.uk/i2c-raspbian-wheezy/info.aspx for more information.")
