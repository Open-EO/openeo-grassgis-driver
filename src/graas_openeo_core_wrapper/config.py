# -*- coding: utf-8 -*-
import os

class Config(object):
    HOST="http://127.0.0.1"
    PORT=8080
    LOCATION="ECAD"
    # LOCATION="LL"
    USER="user"
    PASSWORD="abcdefgh"
    # The database file that stores the graphs
    GRAPH_DB="%s/.graph_db_file.sqlite"%os.environ["HOME"]
