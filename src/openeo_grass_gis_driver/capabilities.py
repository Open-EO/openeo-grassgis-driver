# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

CAPABILITIES = {
    "version": "0.3.0",
    "endpoints": [
        {
            "path": "/",
            "methods": [
                "GET"
            ]
        },
        {
            "path": "/preview",
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
            "path": "/collections/{name}",
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
                "GET", "PATCH", "DELETE"
            ]
        },
        {
            "path": "/output_formats",
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
            "path": "/jobs/{job_id}/results",
            "methods": [
                "GET", "POST", "DELETE"
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
