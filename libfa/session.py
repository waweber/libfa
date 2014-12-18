"""session
"""

import requests

class IRequestProcessor:
    def process_request(self, request, session):
        pass

    def process_response(self, response, session):
        pass

class Session:
    requests_session = None
    request_processors = []

    def __init__(self):
        self.requests_session = requests.Session()

    def add_request_processor(self, proc):
        self.request_processors.append(proc)

    def get_requests_session(self):
        return self.requests_session

    def perform_request(self, method, url, params=None, data=None):
        # Prepare a request object
        req = requests.Request(method, url, params=params,
                data=data)

        # Allow each processor to mutate the request
        for proc in self.request_processors:
            proc.process_request(req, self)

        # Send the request
        prepared_request = self.get_requests_session().prepare_request(req)
        response = self.get_requests_session().send(prepared_request)

        # Allow each processor to mutate the response
        for proc in reversed(self.request_processors):
            proc.process_response(response, self)

        # Return final response
        return response
