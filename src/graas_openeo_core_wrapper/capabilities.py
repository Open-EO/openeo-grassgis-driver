# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import abort, Resource
from flask_restful_swagger_2 import swagger

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

GET_CAPABILITIES_EXAMPLE = ["/data", "/data/{product_id}", "/processes"]

GET_CAPABILITIES_DOC = {
    "summary": "Returns the capabilities, i.e., which OpenEO API features are supported  by the back-end.",
    "description": "The request will ask the back-end which features of the OpenEO API are supported and "
                   "return a simple JSON description with available endpoints.",
    "tags": ["API Information"],
    "responses": {
        "200": {
            "description": "An array of implemented API endpoints",
            "schema": {
                "example": GET_CAPABILITIES_EXAMPLE
            }
        }
    }
}


class Capabilities(Resource):
    @swagger.doc(GET_CAPABILITIES_DOC)
    def get(self, ):
        return make_response(jsonify(GET_CAPABILITIES_EXAMPLE), 200)
