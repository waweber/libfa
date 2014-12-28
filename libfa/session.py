"""session
"""

import requests
from lxml import etree
from lxml.cssselect import CSSSelector
from io import StringIO
from . import exception

class RequestProcessor(object):
    def process_request(self, request, session):
        pass

    def process_response(self, response, session):
        pass

class Session(object):
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

    def perform_request(self, method, url, params=None, data=None,
            headers=None):
        # Prepare a request object
        req = requests.Request(method, self.base_url + url, params=params,
                data=data, cookies={}, headers=headers)

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
        parser = etree.HTMLParser()
        data = etree.parse(StringIO(response.text), parser)

        return data

    def login(self, login_name, password):
        data = {
                "action": "login",
                "retard_protection": "1", # classy
                "name": login_name,
                "pass": password,
                "login": "",
                }

        page = self.perform_request("POST", "/login/", data=data)

        selector = CSSSelector(""".innertable > td:nth-child(1) >
        table:nth-child(1) > tr:nth-child(1) > td:nth-child(1) >
        form:nth-child(2) > table:nth-child(3) > tr:nth-child(2) >
        td:nth-child(1)""")
        err_element = selector(page)

        if len(err_element) != 0:
            raise exception.LoginFailure()


    def logout(self):
        self.perform_request("GET", "/logout/")
