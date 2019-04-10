__all__ = ["cg_render", "get_error_image"]

import os

from nxtools import *
from nxcg import CG

from .common import *


def get_error_image(message):
    logging.error(message)
    cg = CG(1920,1080)
    cg.text(
            message.upper(),
            pos=(0, 800),
            color="red",
            width=1920,
            align=8
        )
    return cg.png

def cg_render(parent, app_name, render_method, **kwargs):
    logging.info(render_method, kwargs)
    app_dir = os.path.join(config["apps_dir"], app_name)
    plugin_dirs = ["plugins", os.path.join(app_dir, "plugins")]
    cg = CG(1920, 1080, plugin_dirs=plugin_dirs)
    cg.app_dir = app_dir
    try:
        exec("cg.{}(**kwargs)".format(render_method))
        data = cg.png
    except Exception:
        log_traceback("Render error")
        data = None
    return data

