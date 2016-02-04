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

"""ruggedpod-api base exception handling."""

import six


class RuggedpodException(Exception):
    message = "An unknown exception occured"
    status_code = 500

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        try:
            self.message = self.msg_fmt % kwargs
        except KeyError:
            # kwargs doesn't match a variable in the message
            # log the issue and the kwargs
            LOG.exception(_('Exception in string format operation'),
                          extra=dict(
                              private=dict(
                                  msg=self.msg_fmt,
                                  args=kwargs
                                  )
                              )
                          )

            if CONF.fatal_exception_format_errors:
                raise

    def __str__(self):
        if six.PY3:
            return self.message
        return self.message.encode('utf-8')

    def __unicode__(self):
        return self.message


class NotFound(RuggedpodException):
    msg_fmt = "The requested object does not exist."
    status_code = 404


class Conflict(RuggedpodException):
    msg_fmt = "Conflict. Reason: %(reason)s"
    status_code = 409


class BadRequest(RuggedpodException):
    msg_fmt = "The request is malformed. Reason: %(reason)s"
    status_code = 400


class BodySyntaxError(BadRequest):
    msg_fmt = "The request is malformed. Reason: The body syntax is not valid"


class ParameterMissing(BadRequest):
    msg_fmt = "The request is malformed. Reason: the parameter %(name)s is missing."


class ConfAttributeMissing(RuggedpodException):
    msg_fmt = "The attribute %(name)s is missing in configuration file"
