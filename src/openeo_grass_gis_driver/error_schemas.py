# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional, Dict
from openeo_grass_gis_driver.schema_base import JsonableObject, EoLinks

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ErrorSchema(JsonableObject):
    """This is the error response schema

    """

    def __init__(self, id: str, code: int, message: str,
                 links: List[Optional[EoLinks]] = list()):

        self.id = id
        self.code = code
        self.message = message
        self.links = links

