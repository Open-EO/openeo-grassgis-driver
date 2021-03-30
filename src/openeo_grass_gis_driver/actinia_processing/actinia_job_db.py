# -*- coding: utf-8 -*-
from openeo_grass_gis_driver.actinia_processing.config import \
   Config as ActiniaConfig
from sqlitedict import SqliteDict

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ActiniaJobDB(SqliteDict):
    """This is the storage of all actinia jobs that where committed
    """
    def __init__(self):
        SqliteDict.__init__(
            self,
            filename=ActiniaConfig.ACTINIA_JOB_DB,
            autocommit=True)
