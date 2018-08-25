# -*- coding: utf-8 -*-
import os

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

class Config(object):
    # Settings for docker swarm image
    HOST="http://actinia.mundialis.de"
    PORT=433
    LOCATION="ECAD"
    # LOCATION="LL"
    LOCATIONS=["LL", "ECAD"]
    USER="demouser"
    PASSWORD="gu3st!pa55w0rd"
    # The database file that stores the graphs
    GRAPH_DB="%s/.graph_db_file.sqlite"%os.environ["HOME"]
