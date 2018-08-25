# -*- coding: utf-8 -*-
from flask_restful import Resource
from .actinia_processing.actinia_interface import ActiniaInterface
from flask import make_response, jsonify
from .graph_db import GraphDB
from .definitions import Job

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

GET_JOBS_ID_DOC = {
    "summary": "Returns information about a submitted job",
    "description": "Returns detailed information about a submitted job including its "
                   "current status and the underlying task",
    "tags": ["Job Management"],
    "parameters": [
        {
            "name": "job_id",
            "in": "path",
            "type": "string",
            "description": "job identifier string",
            "required": True
        }
    ],
    "responses": {
        "200": {"description": "JSON object with job information.", "schema": Job},
        "401": {"$ref": "#/responses/auth_required"},
        "403": {"$ref": "#/responses/access_denied"},
        "404": {"description": "Job with specified identifier is not available"},
        "501": {"$ref": "#/responses/not_implemented"},
        "503": {"$ref": "#/responses/unavailable"}
    }
}

DELETE_JOBS_ID_EXAMPLE = {
    "job_id": "42d5k3nd92mk49dmj294md",
    "status": "scheduled",
    "process_graph": {
        "process_id": "slope",
        "args": {
            "dem": {
                "process_id": "filter_bbox",
                "args": {
                    "imagery": "/data/srtm90m",
                    "srs": "EPSG:4326",
                    "left": 6.301,
                    "right": 7.232,
                    "top": 53.87,
                    "bottom": 50.223
                }
            }
        }
    },
    "submitted": "2017-01-01T09:32:12Z",
    "user_id": "ab32e5f3a2bc2847s2"
}

DELETE_JOBS_ID_DOC = {
    "summary": "Deletes a submitted job",
    "description": "Deleting a job  will cancel execution at the back-end regardless of its status. "
                   "For finished jobs, this will also delete resulting data.",
    "tags": ["Job Management"],
    "parameters": [
        {
            "name": "job_id",
            "in": "path",
            "type": "string",
            "description": "job identifier string",
            "required": True
        }
    ],
    "responses": {
        "200": {
            "description": "JSON object with job information.",
            "examples": {"application/json": DELETE_JOBS_ID_EXAMPLE}
        },
        "401": {"$ref": "#/responses/auth_required"},
        "403": {"$ref": "#/responses/access_denied"},
        "404": {"description": "Job with specified identifier is not available"},
        "501": {"$ref": "#/responses/not_implemented"},
        "503": {"$ref": "#/responses/unavailable"}
    }
}


class JobsJobId(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()
        self.db = GraphDB()

    def get(self, job_id):

        try:
            status, response = self.iface.resource_info(job_id)
            if status == 200:
                process_graph = self.db[job_id]

                info = dict(job_id=job_id,
                            user_id=response["user_id"],
                            status=response["status"],
                            process_graph=process_graph,
                            submitted=response["accept_datetime"],
                            last_update=response["datetime"],
                            consumed_credits=response["time_delta"],
                            job_info=response)

                if "urls" in response and "resources" in response["urls"]:
                    info["resources"] = response["urls"]["resources"]

                return make_response(jsonify(info), 200)
            else:
                process_graph = self.db[job_id]
                info = dict(job_id=job_id,
                            status="error",
                            process_graph=process_graph,
                            job_info=response)

                return make_response(jsonify(info), status)
        except Exception as e:
                return make_response(jsonify({"error": str(e)}), 500)

    def delete(self, job_id):

        try:
            status, response = self.iface.resource_info(job_id)

            if status == 200:

                process_graph = self.db[job_id]
                info = dict(job_id=job_id,
                            user_id="scheduled",
                            status="submitted",
                            process_graph=process_graph,
                            submitted=response["accept_datetime"],
                            last_update=response["datetime"],
                            consumed_credits=response["time_delta"],
                            job_info=response)

                status, response = self.iface.delete_resource(job_id)
                if status != 200:
                    process_graph = self.db[job_id]
                    info = dict(job_id=job_id,
                                status="error",
                                process_graph=process_graph,
                                job_info=response)
                return make_response(jsonify(info), status)
            else:
                process_graph = self.db[job_id]
                info = dict(job_id=job_id,
                            status="error",
                            process_graph=process_graph,
                            job_info=response)

                return make_response(jsonify(info), status)
        except Exception as e:
                return make_response(jsonify({"error": str(e)}), 500)
