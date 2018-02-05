# -*- coding: utf-8 -*-
from graas_openeo_core_wrapper import processes

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class FilterBBoxProcess(object):

    PROCESS_NAME = "filter_bbox"

    DOC = {
        "process_id": "filter_bbox",
        "description": "Drops observations from a collection that are located outside of a given bounding box.",
        "args": {
            "collections": {
                "description": "array of input collections with one element"
            },
            "left": {
                "description": "left boundary (longitude / easting)"
            },
            "right": {
                "description": "right boundary (longitude / easting)"
            },
            "top": {
                "description": "top boundary (latitude / northing)"
            },
            "bottom": {
                "description": "bottom boundary (latitude / northing)"
            },
            "srs": {
                "description": "spatial reference system of boundaries as proj4 or EPSG:12345 like string"
            }
        }
    }
    print("Add entry to PROCESS_DICT", PROCESS_NAME)

    processes.PROCESS_DICT[PROCESS_NAME] = DOC

    def create(self, arguments):
        pass
