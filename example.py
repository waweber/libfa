#!ve/bin/python

import getpass

from libfa.session import Session
from libfa import gallery
from libfa import exception

# New session
s = Session()

login_name = raw_input("Username: ")
password = getpass.getpass()

try:
    s.login(login_name, password)
except exception.LoginFailure as e:
    print("Login failure")
    exit(1)

try:
    items = gallery.get_gallery_by_login_name(s, login_name)
    for item in items:
        print("%d: %s" % (item.id, item.title))
except exception.ParseError as e:
    print("Parsing failed")
    exit(2)

s.logout()

exit(0)
