# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from .definitions import ProcessDescription
from flask_restful import abort, Resource
from .actinia_processing.base import PROCESS_DESCRIPTION_DICT

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

GET_PROCESSES_PROCESS_ID_EXAMPLE = {
    "process_id": "median_time",
    "description": "Applies median aggregation to pixel time series for all bands of the input dataset.",
    "args": {"A": {"description": "input product (time series)"}
             }
}

GET_PROCESSES_PROCESS_ID_DOC = {
    "summary": "Returns further information on a given EO process available at the back-end.",
    "description": "The request will ask the back-end for further details about a process specified by identifier",
    "tags": ["Process Discovery"],
    "parameters": [
        {
            "name": "process_id",
            "in": "path",
            "type": "string",
            "description": "process identifier string such as `NDVI`",
            "required": True
        }
    ],
    "responses": {
        "200": {
            "description": "JSON object with metadata of the EO process.",
            "schema": ProcessDescription,
            "examples": {"application/json": GET_PROCESSES_PROCESS_ID_EXAMPLE}
        },
        "401": {"$ref": "#/responses/auth_required"},
        "404": {"description": "Process with specified identifier is not available"},
        "501": {"$ref": "#/responses/not_implemented"},
        "503": {"$ref": "#/responses/unavailable"}
    }
}


class ProcessesProcessId(Resource):

    def get(self, process_id):

        if process_id not in PROCESS_DESCRIPTION_DICT:
            return make_response(jsonify({"description": "This process does not exist!"}), 400)

        return make_response(jsonify(PROCESS_DESCRIPTION_DICT[process_id]), 200)
