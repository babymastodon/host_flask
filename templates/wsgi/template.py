
import os
import sys

import subprocess
from flask import Flask

#set the python path(s)
SITE_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__),'..','..','sites','{{name}}'))
sys.path.append(SITE_ROOT)

#what are we going to do to secure the server?

from app import app as application

from paste.exceptions.errormiddleware import ErrorMiddleware
application = ErrorMiddleware(application, debug=True)
