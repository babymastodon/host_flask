
import os
import sys

import subprocess
from flask import Flask

#set the python path(s)
SITE_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__),'..','..','sites','{{name}}'))
sys.path.append(SITE_ROOT)

#what are we going to do to secure the server?


def application(environ, start_response):
    try:
        from app import app as student_app
    except NameError, ImportError:
        raise ImportError("Could not find the application entry point. Please make sure that your app.py file has the line: 'app = Flask(__name__)'")
    return student_app(environ, start_response)


from paste.exceptions.errormiddleware import ErrorMiddleware
application = ErrorMiddleware(application, debug=True)
