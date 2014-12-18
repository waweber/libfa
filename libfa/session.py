"""session
"""

import requests
from bs4 import BeautifulSoup

class RequestProcessor:
    def process_request(self, request, session):
        pass

    def process_response(self, response, session):
        pass

class Session:
    base_url = None
    requests_session = None
    request_processors = []

    def __init__(self, base_url="https://www.furaffinity.net"):
        self.requests_session = requests.Session()
        self.base_url = base_url

    def add_request_processor(self, proc):
        self.request_processors.append(proc)

    def get_requests_session(self):
        return self.requests_session

    def perform_request(self, method, url, params=None, data=None):
        # Prepare a request object
        req = requests.Request(method, self.base_url + url, params=params,
                data=data, cookies={})

        # Allow each processor to mutate the request
        for proc in self.request_processors:
            proc.process_request(req, self)

        prepared_request = self.get_requests_session().prepare_request(req)

        # Send the request
        response = self.get_requests_session().send(prepared_request)

        # Allow each processor to mutate the response
        for proc in reversed(self.request_processors):
            proc.process_response(response, self)

        # Parse response
        bs = BeautifulSoup(response.text, "html5lib")

        return bs

