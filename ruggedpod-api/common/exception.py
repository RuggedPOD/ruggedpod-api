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


class BadRequest(RuggedpodException):
    msg_fmt = "The request is malformed. Reason: %(reason)s"
    status_code = 400


class ParameterMissing(BadRequest):
    msg_fmt = "The request is malformed. " \
              "Reason: the parameter %(name)s is missing."


class ConfAttributeMissing(RuggedpodException):
    msg_fmt = "The attribute %(name)s is missing in configuration file"
