# -*- coding: utf-8 -*-
import os
import configparser
from pathlib import Path

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert, Carmen Tawalika"
__copyright__ = "Copyright 2018-2021, Sören Gebbert, mundialis"
__maintainer__ = "mundialis"


# config can be overwritten by mounting *.ini files into folders inside
# the config folder.
if os.environ.get('DEFAULT_CONFIG_PATH'):
    DEFAULT_CONFIG_PATH = os.environ['DEFAULT_CONFIG_PATH']
else:
    DEFAULT_CONFIG_PATH = "/etc/default/openeo-grassgis-driver"
CONFIG_FILES = [str(f) for f in Path(
    DEFAULT_CONFIG_PATH).glob('**/*.ini') if f.is_file()]
GENERATED_CONFIG = DEFAULT_CONFIG_PATH + '/openeo-grassgis-driver.cfg'


class ACTINIA:
    HOST = "https://actinia-dev.mundialis.de"
    PORT = 443
    LOCATIONS = ["nc_spm_08", "utm32n", "latlong_wgs84"]
    USER = "openeo"
    PASSWORD = "EeMob0la"
    # The database file that stores the graphs
    GRAPH_DB = "%s/.graph_db_file.sqlite" % os.environ["HOME"]
    # The database file that stores the jobs
    JOB_DB = "%s/.job_db_file.sqlite" % os.environ["HOME"]
    TOKEN_DB = "%s/.actinia_auth_tokens.sqlite" % os.environ["HOME"]
    # The database file that stores the actinia jobs
    ACTINIA_JOB_DB = "%s/.actinia_job_db_file.sqlite" % os.environ["HOME"]
    SECRET_KEY = "jaNguzeef4seiv5shahchimoo8teiLah"


class Configfile:

    def __init__(self):
        """
        This class will overwrite the config classes above when config files
        named DEFAULT_CONFIG_PATH/**/*.ini exist.
        On first import of the module it is initialized.
        """

        config = configparser.ConfigParser()
        print("Loading config files: " + str(CONFIG_FILES) + " ...")
        config.read(CONFIG_FILES)

        if len(config) <= 1:
            print("Could not find any config file, using default values.")
            return

        # commented out due to
        # OSError: [Errno 30] Read-only file system
        # TODO: is there a better solution to avoid this?
        # with open(GENERATED_CONFIG, 'w') as configfile:
        #     config.write(configfile)
        # print("Configuration written to " + GENERATED_CONFIG)

        # CONFIG
        if config.has_section("ACTINIA"):
            if config.has_option("ACTINIA", "HOST"):
                ACTINIA.HOST = config.get("ACTINIA", "HOST")
            if config.has_option("ACTINIA", "PORT"):
                ACTINIA.PORT = config.get("ACTINIA", "PORT")
            if config.has_option("ACTINIA", "LOCATIONS"):
                ACTINIA.LOCATIONS = config.get("ACTINIA", "LOCATIONS")
            if config.has_option("ACTINIA", "USER"):
                ACTINIA.USER = config.get("ACTINIA", "USER")
            if config.has_option("ACTINIA", "PASSWORD"):
                ACTINIA.PASSWORD = config.get("ACTINIA", "PASSWORD")
            if config.has_option("ACTINIA", "GRAPH_DB"):
                ACTINIA.GRAPH_DB = config.get("ACTINIA", "GRAPH_DB")
            if config.has_option("ACTINIA", "TOKEN_DB"):
                ACTINIA.TOKEN_DB = config.get("ACTINIA", "TOKEN_DB")
            if config.has_option("ACTINIA", "ACTINIA_JOB_DB"):
                ACTINIA.ACTINIA_JOB_DB = config.get(
                    "ACTINIA", "ACTINIA_JOB_DB")
            if config.has_option("ACTINIA", "SECRET_KEY"):
                ACTINIA.SECRET_KEY = config.get("ACTINIA", "SECRET_KEY")


init = Configfile()
Config = ACTINIA
