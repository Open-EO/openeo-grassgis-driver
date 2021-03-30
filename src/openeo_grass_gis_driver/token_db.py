# -*- coding: utf-8 -*-
from openeo_grass_gis_driver.actinia_processing.config import \
     Config as ActiniaConfig
from sqlitedict import SqliteDict

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class TokenDB(SqliteDict):
    """This is the storage of all authorization tokens
    """
    def __init__(self):
        SqliteDict.__init__(
            self,
            filename=ActiniaConfig.TOKEN_DB,
            autocommit=True)
