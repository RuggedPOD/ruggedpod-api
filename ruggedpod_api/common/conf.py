# RuggedPOD management API
#
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

"""
Class to read the configuration file in YAML
"""


from ruggedpod_api.common import exception
from ruggedpod_api.common import yamlutils


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
