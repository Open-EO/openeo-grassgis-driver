# -*- coding: utf-8 -*-
from pprint import pprint
from flask import make_response, jsonify, request
from flask_restful import Resource
from .actinia_processing.base import process_node_to_actinia_process_chain
from .actinia_processing.actinia_interface import ActiniaInterface
from .error_schemas import ErrorSchema
from datetime import datetime

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GraphValidation(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()

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
            result_name, process_list = process_node_to_actinia_process_chain(process_graph)

            if len(ActiniaInterface.PROCESS_LOCATION) == 0 or len(ActiniaInterface.PROCESS_LOCATION) > 1:
                return make_response(jsonify({"description":"Processes can only be defined for a single location!"},
                                             400))

            location = ActiniaInterface.PROCESS_LOCATION.keys()
            location = list(location)[0]

            process_chain = dict(list=process_list,
                                 version="1")

            pprint(process_chain)

            status, response = self.iface.sync_ephemeral_processing_validation(location=location,
                                                                               process_chain=process_chain)
            pprint(response)

            if status == 200:
                return make_response("", 204)
            else:
                es = ErrorSchema(id=str(datetime.now()), code=status, message=str(response))
                return make_response(es.to_json(), status)
        except Exception as e:
                es = ErrorSchema(id=str(datetime.now()), code=400, message=str(e))
                return make_response(es.to_json(), 400)
