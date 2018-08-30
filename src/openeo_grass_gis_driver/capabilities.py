# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import Resource

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

ACTINIA_CAPABILITIES = {
    "version": "0.3.0",
    "endpoints": [
        {
            "path": "/capabilities",
            "methods": [
                "GET"
            ]
        }
    ]
}

GET_CAPABILITIES_DOC = {
    "summary": "Returns the capabilities, i.e., which OpenEO API features are supported  by the back-end.",
    "description": "The request will ask the back-end which features of the OpenEO API are supported and "
                   "return a simple JSON description with available endpoints.",
    "tags": ["API Information"],
    "responses": {
        "200": {
            "description": "An array of implemented API endpoints",
            "schema": {
                "example": ["/data", "/data/{product_id}", "/processes"]
            }
        }
    }
}


class Capabilities(Resource):

    def get(self, ):
        return make_response(jsonify(ACTINIA_CAPABILITIES), 200)
