# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


# https://open-eo.github.io/openeo-api/#operation/capabilities
CAPABILITIES = {
    "api_version": "1.0.0",
    "backend_version": "0.2.0",
    "stac_version": "0.9.0",
    "id": "grass-gis-driver",
    "title": "GRASS GIS Driver",
    "description": "GRASS GIS Driver",
    # "components": {
    #     "securitySchemes": {
    #         "bearerAuth": {
    #             "type": "http",
    #             "scheme": "bearer",
    #             "bearerFormat": "JWT"
    #         }
    #     }
    # },
    # "security": [{
    #     "bearerAuth": []
    # }],
    "endpoints": [
        {
            "path": "/",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/udf_runtimes",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/service_types",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/services",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/credentials/oidc",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/credentials/basic",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/me",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/result",
            "methods": [
                "POST"
            ]
        },
        {
            "path": "/collections",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/collections/{collection_id}",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/processes",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/processes/{process_id}",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/validation",
            "methods": [
                "POST"
            ]
        },
        {
            "path": "/process_graphs",
            "methods": [
                "GET", "POST", "DELETE"
            ]
        },
        {
            "path": "/process_graphs/{process_graph_id}",
            "methods": [
                "GET", "PUT", "DELETE"
            ]
        },
        {
            "path": "/file_formats",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/jobs",
            "methods": [
                "GET", "POST", "DELETE"
            ]
        },
        {
            "path": "/jobs/{job_id}",
            "methods": [
                "GET", "PATCH", "DELETE"
            ]
        },
        {
            "path": "/jobs/{job_id}/estimate",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/jobs/{job_id}/logs",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/jobs/{job_id}/results",
            "methods": [
                "GET", "POST", "DELETE"
            ]
        },
    ],
    "links": [
        {
            "href": "https://openeo.mundialis.de/.well-known/openeo",
            "rel": "version-history",
            "type": "application/json",
            "title": "List of supported openEO versions"
        },
        {
            "href": "https://openeo.mundialis.de/api/v1.0/collections",
            "rel": "data",
            "type": "application/json",
            "title": "List of Datasets"
        }
    ]
}

# deactivated /files and /services POST
"""
        {
            "path": "/files",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/files/{path}",
            "methods": [
                "GET", "PUT", "DELETE"
            ]
        }

        {
            "path": "/services",
            "methods": [
                "GET", "POST"
            ]
        },
        {
            "path": "/services/{service_id}",
            "methods": [
                "GET", "PATCH", "DELETE"
            ]
        },
"""

class Capabilities(Resource):

    def get(self, ):
        return make_response(jsonify(CAPABILITIES), 200)


# https://open-eo.github.io/openeo-api/#operation/list-service-types
SERVICE_TYPES = {}


class ServiceTypes(Resource):

    def get(self, ):
        return make_response(jsonify(SERVICE_TYPES), 200)


# https://open-eo.github.io/openeo-api/#operation/list-service-types
SERVICES = []


class Services(Resource):

    def get(self, ):
        response = dict(services=SERVICES, links=[])
        return make_response(jsonify(response), 200)
