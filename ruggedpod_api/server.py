# RuggedPOD management API
#
# Copyright (C) 2015 Maxime Terras <maxime.terras@numergy.com>
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

import sys

from ruggedpod_api.services import gpio
from ruggedpod_api.api.v1_0.blueprint import api as api_1_0

from flask import Flask

app = Flask(__name__)

app.register_blueprint(api_1_0, url_prefix='/v1')
app.register_blueprint(api_1_0, url_prefix='/v1.0')


if __name__ == "__main__":
    gpio.init()

    if '--debug' in sys.argv:
        app.debug = True
    app.run(host='0.0.0.0', threaded=True)
