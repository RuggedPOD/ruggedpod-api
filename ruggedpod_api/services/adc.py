from ruggedpod_api import config
from ruggedpod_api.common import dependency, singleton


class ADC(object):
    __metaclass__ = singleton.Singleton

    def __init__(self):
        self.ADCHelpers = dependency.lookup('adc_helpers')
        self.ADCPi = dependency.lookup('adc')
        self._adc = None

    def adc(self):
        if self._adc:
            return self._adc
        try:
            i2c = config.get_attr('i2c')
            self._adc = self.ADCPi(self.ADCHelpers().get_smbus(),
                                   i2c['dac_power_consumption_addr'], i2c['dac_other_addr'], 12)
            return self._adc
        except IOError:
            return None

    def read(self, c):
        adc = self.adc()
        if adc is None:
            return 0
        return int(adc.read_raw(c) * 2 / float(1000) - 2.5) * 10 * 24
