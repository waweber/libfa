"""Gallery stuff
"""

from lxml.cssselect import CSSSelector
from .exception import parse_check
from . import exception
import re

class GalleryItem(object):
    id = None
    login_name = None
    preview_url = None
    title = None

@parse_check
def get_by_login_name(session, login_name, gallery_type, page=1):
    url = "/%s/%s/%d/" % (gallery_type, login_name, page)
    data = {
            "perpage": 60,
            "btn": "Next",
            }
    page = session.perform_request("POST", url, data=data)

    # Success test
    selector = CSSSelector(".alt1 > b:nth-child(2)")
    error_element = selector(page)
    if len(error_element) != 0:
        if re.search("could not be found", error_element[0].text) != None:
            raise exception.NotFound(GalleryItem, login_name)

    # Find items
    selector = CSSSelector(".flow > b")
    item_elements = selector(page)

    items = []

    for e in item_elements:
        item = GalleryItem()
        item.login_name = login_name

        # id
        item.id = int(e.get("id")[4:])

        # preview
        selector = CSSSelector("""u:nth-child(1) > s:nth-child(1) >
        a:nth-child(1) > img:nth-child(1)""")
        item.preview_url = selector(e)[0].get("src")

        # Title
        selector = CSSSelector("span:nth-child(2)")
        item.title = selector(e)[0].text

        items.append(item)

    return items

def get_gallery_by_login_name(session, login_name, page=1):
    return get_by_login_name(session, login_name, "gallery", page)

def get_scraps_by_login_name(session, login_name, page=1):
    return get_by_login_name(session, login_name, "scraps", page)

def get_favorites_by_login_name(session, login_name, page=1):
    return get_by_login_name(session, login_name, "favorites", page)
