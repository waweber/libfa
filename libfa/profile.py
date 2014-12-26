"""User
"""

from lxml.cssselect import CSSSelector
from .exception import parse_check
from . import exception
import re

class Profile:
    user_id = None
    full_name = None
    watch_key = None

@parse_check
def get_by_login_name(session, login_name):
    url = "/user/%s/" % login_name

    page = session.perform_request("GET", url)

    # Success test
    selector = CSSSelector(".alt1 > font:nth-child(1)")
    error_element = selector(page)
    if len(error_element) != 0:
        if re.search("cannot be found", error_element[0].text) != None:
            raise exception.NotFound(Profile, login_name)

    profile = Profile()

    # Full name
    selector = CSSSelector("td.ldot:nth-child(1)")
    profile.full_name = selector(page)[0][0].tail.strip()

    # User ID
    selector = CSSSelector(""".innertable > td:nth-child(1) > table:nth-child(1)
    > tr:nth-child(1) > td:nth-child(1) > table:nth-child(2) > tr:nth-child(2) >
    td:nth-child(1) > table > tr:nth-child(3) > td:nth-child(1) >
    a:nth-child(1)""")
    for e in selector(page):
        m = re.search("uid=([0-9]+)", e.get("href"))
        if m:
            profile.user_id = int(m.group(1))
            break

    # Watch key
    selector = CSSSelector(".tab > b:nth-child(9) > a:nth-child(1)")
    key_url = selector(page)[0].get("href")

    m = re.search("\\?key=(.*)", key_url)
    profile.watch_key = m.group(1)

    return profile
