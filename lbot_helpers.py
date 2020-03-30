# lbot_helpers.py

class Error(Exception):
    # Base class for exceptions in this module.
    pass


class APIError(Error):
    # Exception raised if an API call returns an HTTP error.
    def __init__(self, code, url, headers, msg):
        self.code = code
        self.url = url
        self.headers = headers
        self.msg = msg

class InputError(Error):
    # Exception raised for errors in the input.
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message