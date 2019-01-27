# -*- coding: utf-8 -*-
from flask import make_response, jsonify, request
from flask_restful_swagger_2 import swagger
from flask_restful import Resource
from .actinia_processing.base import analyse_process_graph
from .graph_db import GraphDB
from .actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

POST_JOBS_EXAMPLE = {"job_id": "42d5k3nd92mk49dmj294md"}


class Jobs(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()
        self.db = GraphDB()

    def put(self):
        """Modify the existing database by running the job in a persistent mapset

        :return:
        """

        try:

            # Empty the process location
            ActiniaInterface.PROCESS_LOCATION = {}
            request_doc = request.get_json()
            process_graph = request_doc["process_graph"]

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

    def post(self):
        """Run the job in an ephemeral mapset

        :return:
        """

        try:
            # Empty the process location
            ActiniaInterface.PROCESS_LOCATION = {}
            request_doc = request.get_json()
            process_graph = request_doc["process_graph"]
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
