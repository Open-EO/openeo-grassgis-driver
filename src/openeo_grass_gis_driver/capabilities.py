# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify, request

from openeo_grass_gis_driver import __version__

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert, Carmen Tawalika"
__copyright__ = "Copyright 2018-2021, Sören Gebbert, mundialis"
__maintainer__ = "mundialis"


# https://open-eo.github.io/openeo-api/#operation/capabilities
CAPABILITIES = {
    "api_version": "1.0.1",
    "backend_version": __version__,
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
            "href": "https://openeo.example.de/.well-known/openeo",
            "rel": "version-history",
            "type": "application/json",
            "title": "List of supported openEO versions"
        },
        {
            "href": "https://openeo.example.de/api/v1.0/collections",
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


def replace_links_in_capabilities():
    new_url = request.root_url.rstrip('/')

    for i in CAPABILITIES['links']:
        sample_url = i['href']
        split_sample = sample_url.split('/')
        if sample_url.startswith('http'):
            sample_url = "%s//%s" % (split_sample[0], split_sample[2])
        else:
            sample_url = split_sample[0]
        i['href'] = i['href'].replace(sample_url, new_url)
    return CAPABILITIES


class Capabilities(Resource):

    def get(self, ):
        # links need to be replaced here because root_url
        # is only available during a request
        CAPABILITIES = replace_links_in_capabilities()
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
