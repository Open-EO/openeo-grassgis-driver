# -*- coding: utf-8 -*-
from flask import make_response, jsonify, request
from flask_restful_swagger_2 import swagger
from flask_restful import Resource
from .definitions import ProcessGraph
from .actinia_processing.base import analyse_process_graph
from .graph_db import GraphDB
from .actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

POST_JOBS_EXAMPLE = {"job_id": "42d5k3nd92mk49dmj294md"}


POST_JOBS_DOC = {
    "summary": "submits a new job to the back-end",
    "description": "creates a new job from one or more (chained) processes at the back-end, "
                   "which will eventually run the computations",
    "tags": ["Job Management"],
    "parameters": [
        {
            "name": "evaluate",
            "in": "query",
            "description": "Defines how the job should be evaluated. Can be `lazy` (the default), `batch`, or "
                           "`sync` where lazy means that the job runs computations only on download requests "
                           "considering dynamically provided views. Batch jobs are immediately scheduled for "
                           "execution by the back-end. Synchronous jobs will be immediately executed and return "
                           "the result data.",
            "type": "string",
            "enum": ["lazy", "batch", "sync"],
            "default": "lazy",
            "required": False
        },
        {
            "name": "process_graph",
            "in": "body",
            "description": "Description of one or more (chained) processes including their input arguments",
            "schema": ProcessGraph
        },
        {
            "name": "format",
            "in": "query",
            "description": "Description of the desired output format. Required in case `evaluate` is set to `sync`. "
                           "If not specified the format has to be specified in the download request.",
            "type": "string",
            "enum": ["nc", "json", "wcs", "wmts", "tms", "tif", "png", "jpeg"],
            "required": False
        }
    ],
    "responses": {
        "200": {
            "description": "Depending on the job evaluation type, the result of posting jobs can be either a json "
                           "description of the job (for lazy and batch jobs) or a result object such as a NetCDF "
                           "file (for sync jobs).",
            "examples": {
                "application/json": POST_JOBS_EXAMPLE
            }
        },
        "406": {"description": "The server is not capable to deliver the requested format."},
        "501": {"$ref": "#/responses/not_implemented"},
        "503": {"$ref": "#/responses/unavailable"}
    }
}


class Jobs(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()
        self.db = GraphDB()

    @swagger.doc(POST_JOBS_DOC)
    def put(self):
        """Modify the existing database by running the job in a persistent mapset

        :return:
        """

        try:

            # Empty the process location
            ActiniaInterface.PROCESS_LOCATION = {}
            process_graph = request.get_json()
            # Transform the process graph into a process chain and store the input location
            # Check all locations in the process graph
            result_name, process_list = analyse_process_graph(process_graph)

            if len(ActiniaInterface.PROCESS_LOCATION) == 0 or len(ActiniaInterface.PROCESS_LOCATION) > 1:
                return make_response(jsonify({"description":"Processes can only be defined for a single location!"},
                                             400))

            location = ActiniaInterface.PROCESS_LOCATION.keys()
            location = list(location)[0]

            status_code, mapsets = self.iface.list_mapsets(location=location)
            if status_code != 200:
                return make_response(jsonify({"description":"An internal error occurred "
                                                            "while catching mapsets!"}, 400))

            count = 0
            name = "openeo_mapset"
            new_mapset = "%s_%i"%(name, count)
            while new_mapset in mapsets:
                count += 1
                new_mapset = "%s_%i"%(name, count)

            process_chain = dict(list=process_list,
                                 version="1")

            # pprint.pprint(process_chain)

            status, response = self.iface.async_persistent_processing(location=location,
                                                                      mapset=new_mapset,
                                                                      process_chain=process_chain)
            # pprint.pprint(response)

            # Save the process graph into the graph db
            self.db[response["resource_id"]] = process_graph

            if status == 200:
                return make_response(jsonify({"job_id":response["resource_id"],
                                              "job_info":response}), status)
            else:
                return make_response(jsonify(response), status)
        except Exception as e:
                return make_response(jsonify({"error": str(e)}), 400)

    @swagger.doc(POST_JOBS_DOC)
    def post(self):
        """Run the job in an ephemeral mapset

        :return:
        """

        try:
            # Empty the process location
            ActiniaInterface.PROCESS_LOCATION = {}
            process_graph = request.get_json()
            # Transform the process graph into a process chain and store the input location
            # Check all locations in the process graph
            result_name, process_list = analyse_process_graph(process_graph)

            if len(ActiniaInterface.PROCESS_LOCATION) == 0 or len(ActiniaInterface.PROCESS_LOCATION) > 1:
                return make_response(jsonify({"description":"Processes can only be defined for a single location!"},
                                             400))

            location = ActiniaInterface.PROCESS_LOCATION.keys()
            location = list(location)[0]

            process_chain = dict(list=process_list,
                                 version="1")

            # pprint.pprint(process_chain)

            status, response = self.iface.async_ephemeral_processing_export(location=location,
                                                                            process_chain=process_chain)
            # pprint.pprint(response)

            # Save the process graph into the graph db
            self.db[response["resource_id"]] = process_graph

            if status == 200:
                return make_response(jsonify({"job_id":response["resource_id"],
                                              "job_info":response}), status)
            else:
                return make_response(jsonify(response), status)
        except Exception as e:
                return make_response(jsonify({"error": str(e)}), 400)
