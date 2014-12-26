"""Watches
"""

from . import profile
from lxml.cssselect import CSSSelector

def get_watches_by_user_id(session, user_id, page=1):
    url = "/budslist/"
    params = {
            "uid": user_id,
            "mode": "watches",
            "page": page - 1,
            }
    page = session.perform_request("POST", url, params=params)
    selector = CSSSelector(".artist_name")
    elements = selector(page)

    watches = []

    for e in elements:
        watches.append(e.text)

    return watches

def get_watches_by_login_name(session, login_name, page=1):
    p = profile.get_by_login_name(session, login_name)
    return get_watches_by_user_id(session, p.user_id, page)

def get_watchers_by_user_id(session, user_id, page=1):
    url = "/budslist/"
    params = {
            "uid": user_id,
            "mode": "watched_by",
            "page": page - 1,
            }
    page = session.perform_request("POST", url, params=params)
    selector = CSSSelector(".artist_name")
    elements = selector(page)

    watches = []

    for e in elements:
        watches.append(e.text)

    return watches

def get_watchers_by_login_name(session, login_name, page=1):
    p = profile.get_by_login_name(session, login_name)
    return get_watchers_by_user_id(session, p.user_id, page)
