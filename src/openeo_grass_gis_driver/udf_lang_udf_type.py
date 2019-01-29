# -*- coding: utf-8 -*-
from .actinia_processing.actinia_interface import ActiniaInterface
from flask import make_response, jsonify
from .process_graph_db import GraphDB
# from .actinia_processing import udf_reduce_time
from flask_restful import Resource

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


python_udfs = dict(python={})
# python_udfs["python"][udf_reduce_time.PROCESS_NAME] = udf_reduce_time.DOC

GET_UDF_TYPE_EXAMPLE = None

GET_UDF_TYPE_DOC = {
    "summary": "Returns the process description of UDF schemas, which offer different possibilities how "
               "user-defined scripts can be applied to the data.",
    "tags": ["UDF"],
    "parameters": [
        {
            "name": "lang",
            "in": "path",
            "description": "Language identifier such as `R`",
            "type": "string",
            "enum": ["python", "R"],
            "required": True
        },
        {
            "name": "udf_type",
            "in": "path",
            "type": "string",
            "description": "The UDF types define how UDFs can be exposed to the data, how they can be parallelized, "
                           "and how the result schema should be structured.",
            "enum": ["apply_pixel", "apply_scene", "reduce_time", "reduce_space", "window_time", "window_space",
                     "window_spacetime", "aggregate_time", "aggregate_space", "aggregate_spacetime"],
            "required": True
        }
    ],
    "responses": {
        "200": {
            "description": "Process description",
            "schema": UDFDescription,
            "examples": {"application/json": GET_UDF_TYPE_EXAMPLE}
        },
        "401": {"$ref": "#/responses/auth_required"},
        "403": {"$ref": "#/responses/access_denied"},
        "404": {"description": "UDF type with specified identifier is not available"},
        "501": {"description": "This API feature, language or UDF type is not supported by the back-end."},
        "503": {"$ref": "#/responses/unavailable"}
    }
}


class UdfType(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()
        self.db = GraphDB()

    def get(self, lang, udf_type):

        if lang not in python_udfs:
            return make_response(jsonify({"description": "UDF type with "
                                                         "specified identifier is not available"}), 404)

        if udf_type not in python_udfs[lang]:
            return make_response(jsonify({"description": "UDF type with "
                                                         "specified identifier is not available"}), 404)

        return make_response(jsonify(python_udfs[lang][udf_type]), 200)
