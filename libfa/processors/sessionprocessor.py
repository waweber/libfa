"""Assumes an existing session
"""

class SessionProcessor:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def process_request(self, request, session):
        request.cookies["a"] = self.a
        request.cookies["b"] = self.b

    def process_response(self, response, session):
        pass
