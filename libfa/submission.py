"""Submission
"""

from lxml.cssselect import CSSSelector
from lxml import etree
import datetime
import re
from . import rating

class Submission:
    id = None
    author_user_name = None
    author_display_name = None
    title = None
    date = None
    media_url = None
    text = None

    favorites = None
    comments = None
    views = None

    rating = None


def get_submission(session, submission_id):
    url = "/view/%s/" % (submission_id)
    page = session.perform_request("GET", url)

    sub = Submission()
    sub.id = submission_id

    # Title
    selector = CSSSelector("table.maintable:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > b:nth-child(1)")
    sub.title = selector(page)[0].text

    # Author
    selector = CSSSelector("table.maintable:nth-child(6) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(2)")
    sub.author_display_name = selector(page)[0].text

    # Media url
    # This one's hacky
    selector = CSSSelector("div.alt1 > b > a")
    for e in selector(page):
        if e.text.strip() == "Download":
            sub.media_url = e.get("href")

    # Date
    selector = CSSSelector(".popup_date")
    date_str = selector(page)[0].get("title")
    # remove english ordinal
    date_str = re.sub("([0-9]{1,2})(st|nd|rd|th)", "\\1", date_str)
    sub.date = datetime.datetime.strptime(date_str, "%B %d, %Y %I:%M %p")

    # Favs
    selector = CSSSelector("""table.maintable:nth-child(6) > tr:nth-child(1) >
    td:nth-child(2) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(1) >
    b:nth-child(14)""")
    sub.favorites = int(selector(page)[0].tail)

    # Comments
    selector = CSSSelector("""table.maintable:nth-child(6) > tr:nth-child(1) >
    td:nth-child(2) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(1) >
    b:nth-child(16)""")
    sub.comments = int(selector(page)[0].tail)

    # Views
    selector = CSSSelector("""table.maintable:nth-child(6) > tr:nth-child(1) >
    td:nth-child(2) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(1) >
    b:nth-child(18)""")
    sub.views = int(selector(page)[0].tail)

    # Text
    selector = CSSSelector("""table.maintable:nth-child(6) > tr:nth-child(2) >
    td:nth-child(1)""")
    text_element = selector(page)[0]

    text_str = ""
    for e in text_element[3:]:
        text_str += etree.tostring(e, with_tail=True)

    sub.text = text_str

    # Get rating
    selector = CSSSelector("""table.maintable:nth-child(6) > tr:nth-child(1) >
    td:nth-child(2) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(1) >
    div:nth-child(26) > img:nth-child(1)""")
    rating_str = selector(page)[0].get("alt")
    if "General" in rating_str:
        sub.rating = rating.GENERAL
    elif "Mature" in rating_str:
        sub.rating = rating.MATURE
    elif "Adult" in rating_str:
        sub.rating = rating.ADULT

    return sub
