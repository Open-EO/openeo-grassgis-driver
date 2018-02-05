# -*- coding: utf-8 -*-
from graas_openeo_core_wrapper import process_definitions

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class FilterDataRangeProcess(object):

    PROCESS_NAME = "filter_daterange"

    DOC = {
        "process_id": "filter_daterange",
        "description": "Drops observations from a collection that have been captured before"
                       " a start or after a given end date.",
        "args": {
            "collections": {
                "description": "array of input collections with one element"
            },
            "from": {
                "description": "start date"
            },
            "to": {
                "description": "end date"
            }
        }
    }

    process_definitions.PROCESS_DICT[PROCESS_NAME] = DOC

    def create(self, process_description):
        pass
