import os
import json
import yaml

from nxtools.logging import *

__all__ = ["config", "apps_config", "login_helper"]

logging.user = "CGTool"

base_dir = os.path.abspath(os.getcwd())
site_dir = os.path.join(base_dir, "site")
apps_dir = os.path.join(base_dir, "apps")
config_path = os.path.join(base_dir, "settings.json")

config = {
    "base_dir"    : base_dir,
    "site_dir"    : site_dir,
    "apps_dir"    : apps_dir,
}

if os.path.exists(config_path):
    logging.info("Using settings file {}".format(config_path))
    try:
        config.update(json.load(open(config_path)))
    except Exception:
        log_traceback()
        critical_error("Unable to open configuration file")
else:
    logging.info("Using default config")


def get_options_data(arg):
    if arg.get("data_command", False):
        try:
            return json.loads(os.popen(arg["data_command"]).read())
        except:
            log_traceback()
    return []


class AppsConfig(object):
    def __init__(self, apps_dir):
        self.data = {}
        self.apps_dir = apps_dir
        self.load()

    def load(self):
        data = {}
        for app_name in os.listdir(self.apps_dir):
            app_dir = os.path.join(self.apps_dir, app_name)
            if not os.path.isdir(app_dir):
                continue
            manifest_path = os.path.join(app_dir, "manifest.yaml")
            if not os.path.exists(manifest_path):
                continue
            try:
                app_config = yaml.safe_load(open(manifest_path))
            except Exception:
                log_traceback()
                continue
            data[app_name] = app_config
            logging.info("Loaded app manifest {}".format(app_name))
        self.data = data

    def __getitem__(self, key):
        return self.data[key]

    def keys(self):
        return self.data.keys()


apps_config = AppsConfig(config["apps_dir"])


def login_helper(login, password):
    if login not in apps_config.keys():
        logging.warning("No such app", login)
        return False
    if password != apps_config[login]["password"]:
        return False
    return {
            "name" : login
        }
