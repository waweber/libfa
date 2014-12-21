"""User
"""

from lxml.cssselect import CSSSelector

class User:
    login_name = None
    user_name = None
    icon_url = None

def user_name_to_login_name(user_name):
    login_name = user_name.replace("_", "").lower()
    return login_name

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

