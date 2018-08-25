# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import Resource
from .actinia_processing.base import PROCESS_DESCRIPTION_DICT
from .definitions import ProcessListEntry

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


GET_PROCESSES_EXAMPLE = [
    {
        "process_id": "NDVI",
        "description": "Computes the normalized difference vegetation index (NDVI) for "
                       "all pixels of the input dataset."
    },
    {
        "process_id": "median_time",
        "description": "Applies median aggregation to pixel time series for all bands of the input dataset."
    }
]

GET_PROCESSES_DOC = {
    "summary": "Returns processes supported by the back-end",
    "description": "The request will ask the back-end for available processes and will return an array "
                   "of available processes with their unique identifiers and description",
    "tags": ["Process Discovery"],
    "parameters": [
        {
            "name": "qname",
            "in": "query",
            "type": "string",
            "description": "string expression to search for available processes by name",
            "required": False
        }
    ],
    "responses": {
        "200": {
            "description": "An array of EO processes including their unique identifiers and a description.",
            "schema": {
                "type": "array",
                "items": ProcessListEntry
            },
            "examples": GET_PROCESSES_EXAMPLE
        },
        "401": {"$ref": "#/responses/auth_required"},
        "501": {"$ref": "#/responses/not_implemented"},
        "503": {"$ref": "#/responses/unavailable"}
    }
}


class Processes(Resource):

    def get(self):
        return make_response(jsonify(list(PROCESS_DESCRIPTION_DICT.keys())), 200)
