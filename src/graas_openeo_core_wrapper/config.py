# -*- coding: utf-8 -*-
import os

class Config(object):
    # Settings for docker swarm image
    HOST="http://graas"
    # HOST="http://localhost"
    PORT=8080
    LOCATION="ECAD"
    # LOCATION="LL"
    LOCATIONS=["LL", "ECAD"]
    USER="user"
    PASSWORD="abcdefgh"
    # The database file that stores the graphs
    GRAPH_DB="%s/.graph_db_file.sqlite"%os.environ["HOME"]
