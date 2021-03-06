# RuggedPOD management API
#
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

import json

from flask import Blueprint

from ruggedpod_api.common import exception
from ruggedpod_api.services import auth

api = Blueprint('v2_0', __name__)


@api.errorhandler(auth.AuthenticationFailed)
@api.errorhandler(exception.NotFound)
@api.errorhandler(exception.Conflict)
@api.errorhandler(exception.BadRequest)
@api.errorhandler(exception.NoContent)
@api.errorhandler(exception.BodySyntaxError)
@api.errorhandler(exception.ParameterMissing)
def handle_error(error):
    data = {
        "message": error.message,
        "code": error.status_code
    }
    return json.dumps(data), error.status_code
