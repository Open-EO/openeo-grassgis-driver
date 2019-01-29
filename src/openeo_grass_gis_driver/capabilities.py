# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import Resource

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

CAPABILITIES = {
    "api_version": "0.4.0",
    "backend_version": "0.1.0",
    "title": "GRASS GIS Driver",
    "description": "GRASS GIS Driver",
    "endpoints": [
        {
            "path": "/capabilities",
            "methods": [
                "GET"
            ]
        }
    ]
}


class Capabilities(Resource):

    def get(self, ):
        return make_response(jsonify(CAPABILITIES), 200)


SERVICE_TYPES = {}


class ServiceTypes(Resource):

    def get(self, ):
        return make_response(jsonify(SERVICE_TYPES), 200)
