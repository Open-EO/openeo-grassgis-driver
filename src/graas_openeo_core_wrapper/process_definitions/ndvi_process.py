# -*- coding: utf-8 -*-
from graas_openeo_core_wrapper import process_definitions

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"



PROCESS_NAME = "NDVI"

DOC = {
    "process_id": "NDVI",
    "description": "Compute the NDVI based on the red and nir bands of the input dataset.",
    "args": {
        "collections": {
            "description": "array of input collections with one element"
        },
        "red": {
            "description": "reference to the red band"
        },
        "nir": {
            "description": "reference to the nir band"
        }
    }
}

process_definitions.PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC
