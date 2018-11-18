# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional, Dict
from .schema_base import JsonableObject, EoLinks

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class JobInformation(JsonableObject):
    """Information about a job
    """

    def __init__(self):
        pass
