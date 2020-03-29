#!/usr/bin/env python3

import rex
import cherrypy

from cgtool import *
from cherryadmin import *

def application(environ, start_response):
    app = CherryAdmin(start_engine=False, **cgtool_config)
    return cherrypy.tree(environ, start_response)

if __name__ == "__main__":
    cgtool = CherryAdmin(**cgtool_config)
