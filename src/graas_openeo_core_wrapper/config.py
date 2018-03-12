# -*- coding: utf-8 -*-
import os

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

class Config(object):
    # Settings for docker swarm image
    HOST="http://graas"
    # HOST="http://openeo.mundialis.de"
    PORT=8080
    LOCATION="ECAD"
    # LOCATION="LL"
    LOCATIONS=["LL", "ECAD"]
    USER="user"
    PASSWORD="abcdefgh"
    # The database file that stores the graphs
    GRAPH_DB="%s/.graph_db_file.sqlite"%os.environ["HOME"]
