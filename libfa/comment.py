"""Comment
"""

from lxml.cssselect import CSSSelector
from lxml import etree
from . import user
import datetime

class Comment:
    id = None
    author = None
    date = None
    title = None
    text = None

def parse_all_from_submission_page(page):
    selector = CSSSelector("table.container-comment")
    comment_elements = selector(page)

    comments = []

    for e in comment_elements:
        comment = Comment()

        # id
        selector = CSSSelector("""tr:nth-child(2) > th:nth-child(2) >
        h4:nth-child(1) > a:nth-child(1)""")
        id_text = selector(e)[0].get("href")
        comment.id = int(id_text[5:])

        # Title
        selector = CSSSelector("""tr:nth-child(2) > th:nth-child(2) >
        h4:nth-child(1) > a:nth-child(1) > i:nth-child(1) > b:nth-child(1)""")
        comment.title = selector(e)[0].text

        # Date
        # TODO: weird timezone stuff
        comment.date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(e.get("data-timestamp")))

        # Text
        selector = CSSSelector("tr:nth-child(3) > td:nth-child(2)")
        comment_element = selector(e)[0]
        comment_text = comment_element.text

        for child in comment_element[:-2]:
            comment_text += etree.tostring(child, with_tail=True)

        comment.text = comment_text

        # Parse author
        comment.author = user.parse_from_comment(e)

        comments.append(comment)

    return comments
