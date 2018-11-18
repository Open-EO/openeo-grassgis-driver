# -*- coding: utf-8 -*-
from pprint import pprint
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



class GraphValidation(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()
        self.db = GraphDB()

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

            # pprint(process_chain)

            status, response = self.iface.sync_ephemeral_processing_validation(location=location,
                                                                               process_chain=process_chain)
            pprint(response)

            if status == 200:
                return make_response("", 204)
            else:
                return make_response(jsonify(response), status)
        except Exception as e:
                return make_response(jsonify({"error": str(e)}), 400)
