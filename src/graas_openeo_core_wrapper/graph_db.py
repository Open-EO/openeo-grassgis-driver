# -*- coding: utf-8 -*-
from flask import json
from graas_openeo_core_wrapper.config import Config as GRaaSConfig
import requests
from sqlitedict import SqliteDict

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GraphDB(SqliteDict):
    """This is the storage of the process graphs that were commited for processing

    """
    def __init__(self):
        SqliteDict.__init__(self, filename=GRaaSConfig.GRAPH_DB, autocommit=True)
