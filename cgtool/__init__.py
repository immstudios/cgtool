import os
import json
import cherrypy

from nxtools import *

from .common import *
from .app import CGToolEditorHandler, CGToolRenderHandler

def site_context_helper():
    return {
            "name" : "cgtool",
            "title" : "CGTool",
            "author" : "imm studios, z.s.",
            "description" : "Template based graphics editor and renderer",
            "css" : [
#                    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
 #                   "https://cdnjs.cloudflare.com/ajax/libs/gijgo/1.9.10/combined/css/gijgo.min.css",
 #                   "https://use.fontawesome.com/releases/v5.5.0/css/solid.css",
 #                   "https://use.fontawesome.com/releases/v5.5.0/css/regular.css",
 #                   "https://use.fontawesome.com/releases/v5.5.0/css/fontawesome.css",
 #                   "https://fonts.googleapis.com/css?family=Roboto:400,500,700&amp;subset=latin-ext",

  #                  "/static/css/switch.css",
                                       "https://static.nebulabroadcast.com/nebula/css/nebula.css",
                    "/static/css/style.css"
                ],
            "js" : [
                    "https://code.jquery.com/jquery-3.3.1.min.js",
                    "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js",
                    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js",
                    "https://cdnjs.cloudflare.com/ajax/libs/gijgo/1.9.10/combined/js/gijgo.min.js",
                    "/static/js/main.js",
                ],
        }

def page_context_helper():
    return {}

def user_context_helper(meta):
    return meta

cgtool_config = {
        "port" : 8400,
        "minify_html" : True,
        "static_dir" : "site/static",
        "templates_dir" : "site/templates",
        "sessions_dir" : "/tmp/cgtool-sessions",
        "login_helper" : login_helper,
        "site_context_helper" : site_context_helper,
        "page_context_helper" : page_context_helper,
        "user_context_helper" : user_context_helper,
        "blocking" : True,
        "views" : {
                "index" : CGToolEditorHandler,
                "render" : CGToolRenderHandler,
            }
    }

for key in [

            "host",
            "port",
            "static_dir",
            "templates_dir",
        ]:
    if key in config:
        cgtool_config[key] = config[key]
