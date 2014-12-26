"""Exceptions
"""

class LoginFailure(Exception):
    pass

class ParseError(Exception):
    pass

def parse_check(f):
    def wrapped_func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (KeyError, IndexError, ValueError) as e:
            raise ParseError()
    return wrapped_func
