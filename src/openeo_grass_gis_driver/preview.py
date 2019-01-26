# -*- coding: utf-8 -*-
import time
import datetime
from flask import make_response, jsonify, request, json
from flask_restful import Resource
from openeo_grass_gis_driver.actinia_processing.base import analyse_process_graph
from openeo_grass_gis_driver.graph_db import GraphDB
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Preview(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()
        self.db = GraphDB()

    def post(self):
        """Run the job in an ephemeral mapset synchronously for 30 seconds. After 30 seconds the job
        will be killed on the actinia server and the response will be an error report.
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
            print(status, response)
            response = self.wait_until_finished(response=response, max_time=5)

            if status == 200:
                return make_response(jsonify({"job_id":response["resource_id"],
                                              "job_info":response}), status)
            else:
                return make_response(jsonify(response), status)
        except Exception as e:
            return make_response(jsonify({"preview error": str(e)}), 400)

    def wait_until_finished(self, response, max_time = 30):
        """Poll the status of a resource and assert its finished HTTP status

        The response will be checked if the resource was accepted. Hence it must always be HTTP 200 status.

        The status URL from the response is then polled until status: finished, error or terminated.
        The result of the poll can be checked against its HTTP status and its GRaaS status message.

        Args:
            response: The accept response
            max_time (int): The maximum time to wait, until the job gets killed

        Returns: response

        """
        # Check if the resource was accepted

        resource_id = response["resource_id"]
        start_time = time.time()

        while True:
            status, resp_data = self.iface.resource_info(resource_id)

            if "status" not in resp_data:
                raise Exception("wrong return values %s" % str(resp_data))
            if resp_data["status"] == "finished" or \
                    resp_data["status"] == "error" or \
                    resp_data["status"] == "terminated":
                break
            time.sleep(1)

            current_time = time.time()
            if current_time - start_time > max_time:
                status_code, data = self.iface.delete_resource(resource_id=resource_id)

                if status_code != 200:
                    raise Exception(f"Unable to terminate job, error: {data}")

        return resp_data
