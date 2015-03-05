"""
Class to read the configuration file in YAML
"""


from common import exception
from common import yamlutils


class YmlConf(object):
    cfg_dict = {}

    def __init__(self, filepath):
        with open(filepath, 'r') as ymlfile:
            self.cfg_dict = yamlutils.load(ymlfile)

    def get_attr(self, attr_name):
        try:
            return self.cfg_dict[attr_name]
        except KeyError:
            raise exception.ConfAttributeMissing(name=attr_name)
