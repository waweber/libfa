"""User
"""

from lxml.cssselect import CSSSelector
from .exception import parse_check

class User:
    login_name = None
    user_name = None
    icon_url = None

def user_name_to_login_name(user_name):
    login_name = user_name.replace("_", "").lower()
    return login_name

@parse_check
def get_by_login_name(session, login_name):
    url = "/user/%s/" % login_name

    page = session.perform_request("GET", url)

    user = User()
    user.login_name = login_name

    # User name
    selector = CSSSelector("td.lead:nth-child(2) > b:nth-child(1)")
    user.user_name = selector(page)[0].text[1:]

    # Icon
    selector = CSSSelector(""".innertable > td:nth-child(1) > table:nth-child(1)
    > tr:nth-child(1) > td:nth-child(1) > table:nth-child(2) > tr:nth-child(1) >
    td:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(1) >
    table:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1)
    > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1) > img:nth-child(1)""")
    user.icon_url = selector(page)[0].get("src")

    return user

@parse_check
def parse_from_submission_page(page):
    user = User()

    # user name
    selector = CSSSelector("""table.maintable:nth-child(6) > tr:nth-child(1) >
    td:nth-child(1) > a:nth-child(2)""")
    user.user_name = selector(page)[0].text

    # login name
    user.login_name = user_name_to_login_name(user.user_name)

    # Icon
    selector = CSSSelector("""table.maintable:nth-child(6) > tr:nth-child(2) >
    td:nth-child(1) > a:nth-child(1) > img:nth-child(1)""")
    user.icon_url = selector(page)[0].get("src")

    return user

@parse_check
def parse_from_comment(comment):
    user = User()

    # User name
    selector = CSSSelector("""tr:nth-child(1) > td:nth-child(3) >
    div:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > b:nth-child(1)""")
    user.user_name = selector(comment)[0].text

    # login name
    user.login_name = user_name_to_login_name(user.user_name)

    # Icon
    selector = CSSSelector("""tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)
    > img:nth-child(1)""")
    user.icon_url = selector(comment)[0].get("src")

    return user
