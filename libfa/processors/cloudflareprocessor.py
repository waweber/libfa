"""Cloudflare processor
"""

from ..session import RequestProcessor

class CloudflareProcessor(RequestProcessor):
    def __init__(self, ua, duid, clearance):
        self.ua = ua
        self.duid = duid
        self.clearance = clearance

    def process_request(self, request, session):
        request.headers["User-Agent"] = self.ua
        request.cookies["__cfduid"] = self.duid
        request.cookies["cf_clearance"] = self.clearance

    def process_response(self, response, session):
        pass
