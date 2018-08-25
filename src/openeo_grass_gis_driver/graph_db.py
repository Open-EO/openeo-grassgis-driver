# -*- coding: utf-8 -*-
from .actinia_processing.config import Config as ActiniaConfig
from sqlitedict import SqliteDict

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GraphDB(SqliteDict):
    """This is the storage of the process graphs that were commited for processing

    """
    def __init__(self):
        SqliteDict.__init__(self, filename=ActiniaConfig.GRAPH_DB, autocommit=True)
