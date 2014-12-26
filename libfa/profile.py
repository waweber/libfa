"""User
"""

from lxml.cssselect import CSSSelector
from .exception import parse_check
import re

class Profile:
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

    # Watch key
    selector = CSSSelector(".tab > b:nth-child(9) > a:nth-child(1)")
    key_url = selector(page)[0].get("href")

    m = re.search("\\?key=(.*)", key_url)
    profile.watch_key = m.group(1)

    return profile
