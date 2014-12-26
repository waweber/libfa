"""User
"""

from lxml.cssselect import CSSSelector
from .exception import parse_check
import re

class Profile:
    user_id = None
    full_name = None
    watch_key = None

@parse_check
def get_by_login_name(session, login_name):
    url = "/user/%s/" % login_name

    page = session.perform_request("GET", url)

    profile = Profile()

    # Full name
    selector = CSSSelector("td.ldot:nth-child(1)")
    profile.full_name = selector(page)[0][0].tail.strip()

    # User ID
    selector = CSSSelector(""".innertable > td:nth-child(1) > table:nth-child(1)
    > tr:nth-child(1) > td:nth-child(1) > table:nth-child(2) > tr:nth-child(2) >
    td:nth-child(1) > table:nth-child(5) > tr:nth-child(3) > td:nth-child(1) >
    a:nth-child(1)""")
    buds_url = selector(page)[0].get("href")
    m = re.search("uid=([0-9]+)", buds_url)
    profile.user_id = int(m.group(1))

    # Watch key
    selector = CSSSelector(".tab > b:nth-child(9) > a:nth-child(1)")
    key_url = selector(page)[0].get("href")

    m = re.search("\\?key=(.*)", key_url)
    profile.watch_key = m.group(1)

    return profile
