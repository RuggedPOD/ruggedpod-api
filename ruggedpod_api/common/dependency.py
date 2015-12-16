# RuggedPOD management API
#
# Copyright (C) 2015 Pierre Padrixe <pierre.padrixe@gmail.com>
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

"""
dependency injection utilities
"""

import sys
import os

from ruggedpod_api import config


di = config.get_attr('dependency_injection')
profile = di['profile']
dependencies = di['dependencies']


def import_module(import_str):
    """Import a module."""
    __import__(import_str)
    return sys.modules[import_str]


def lookup(name):
    """Get an object from its logical name"""
    dependency = dependencies[name][profile]
    import_str = dependency['import']

    if 'from' in dependency:
        from_str = dependency['from']
        obj = __import__(import_str, fromlist=[from_str])
        return getattr(obj, from_str)

    return import_module(import_str)
