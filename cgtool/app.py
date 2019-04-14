import os
import jinja2
import yaml
import cherrypy
import json
import time

from nxtools import *
from cherryadmin import *

from .common import *
from .render import *

system_params = [
        "layout_name",
        "cgtool_action"
    ]

class CGToolEditorHandler(CherryAdminView):
    def build(self, *args, **kwargs):

        # Special actions (do something and redirect to index)

        if "cgtool_action" in kwargs:
            action = kwargs["cgtool_action"]
            if action == "reload":
                apps_config.load()
            raise cherrypy.HTTPRedirect("/")

        # Current app and layout

        app_name = self["user"]["name"]
        app_layouts = apps_config[app_name]["layouts"]
        for layout in app_layouts:
            if not "visible" in layout:
                layout["visible"] = True

        layout = app_layouts[0]
        if kwargs.get("layout_name", False):
            layout_name = kwargs["layout_name"]
            for l in app_layouts:
                if l["name"] == layout_name:
                    layout = l
                    break


        self["layouts"] = app_layouts
        self["layout"] = layout

        # Load cookie data

        cookie_name = str(app_name + "_" + layout["name"])
        try:
            cookie = cherrypy.request.cookie
            cookie_data = json.loads(cookie[cookie_name].value)
        except Exception:
            cookie_data = {}
        cookie_data = {}

        # Render params

        params = {}
        for param in layout.get("params", []):
            pname = param["name"]
            if pname in kwargs:
                if param.get("type", "text") == "boolean":
                    params[pname] = str(int(kwargs[pname] == "on"))
                else:
                    params[pname] = kwargs[pname]
            elif pname in cookie_data:
                params[pname] = cookie_data[pname]
            else:
                params[pname] = param["default"]
                if param.get("type", "text") == "text":
                    params[pname] = params[pname] or ""
        self["params"] = params

        # Save cookie data

        cookie = cherrypy.response.cookie
        cookie[cookie_name] = json.dumps(params)
        cookie[cookie_name]['path'] = '/'
        cookie[cookie_name]['max-age'] = 3600*24
        cookie[cookie_name]['version'] = 1



class CGToolRenderHandler(CherryAdminRawView):
    def auth(self):
        return True

    def build(self, *args, **kwargs):
        start_time = time.time()
        self["mime"] = "image/png"
        try:
            app_name, layout_name = args[1:]
        except ValueError:
            self.body = get_error_image("Incorrect number of arguments")
            return

        if not app_name in apps_config.keys():
            self.body = get_error_image("Unknown app name")
            return

        for data in apps_config[app_name]["layouts"]:
            if data["name"] == layout_name:
                layout = data
                break
        else:
            self.body = get_error_image("Unknown layout requested")
            return

        render_params = {}
#        for param in layout["params"]:
#            if param.get("default", False):
#                render_params[param["name"]] = param["default"]

        for param in kwargs:
            if param not in system_params:
                render_params[param] = kwargs[param]

        result = cg_render(self, app_name, layout["method"], **render_params)
        if result:
            self.body = result
        else:
            cherrypy.response.status = 500
            self.body = get_error_image("Render error")
        logging.goodnews("Render (layout {}) finished in {:.02f}s".format(layout_name, time.time() - start_time))

