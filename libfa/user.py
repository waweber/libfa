"""User
"""

from lxml.cssselect import CSSSelector

class User:
    user_name = None
    display_name = None
    full_name = None
    icon_url = None

def get_user_info(session, user_name):
    url = "/user/%s/" % (user_name)

    page = session.perform_request("GET", url)

    user = User()
    user.user_name = user_name

    # Search for display_name
    selector = CSSSelector("td.lead:nth-child(2) > b:nth-child(1)")
    user.display_name = selector(page)[0].text[1:]

    # Full name
    selector = CSSSelector("td.ldot:nth-child(1)")
    user.full_name = selector(page)[0][0].tail.strip()

    # Icon
    selector = CSSSelector("img[alt=\"Avatar [ %s ]\"]" % user_name)
    user.icon_url = selector(page)[0].get("src")

    return user
