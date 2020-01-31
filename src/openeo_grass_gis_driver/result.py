# -*- coding: utf-8 -*-
import time
import sys
import traceback
from flask import make_response, jsonify, request, Response
from openeo_grass_gis_driver.actinia_processing.base import Graph
from openeo_grass_gis_driver.process_graph_db import GraphDB
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.actinia_processing.config import Config as ActiniaConfig
from openeo_grass_gis_driver.authentication import ResourceBase
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Result(ResourceBase):

    def __init__(self):
        ResourceBase.__init__(self)
        self.iface = ActiniaInterface()
        self.iface.set_auth(ActiniaConfig.USER, ActiniaConfig.PASSWORD)
        self.db = GraphDB()

    def post(self):
        """Run the job in an ephemeral mapset synchronously for 10 seconds. After 10 seconds the running job
        will be killed on the actinia server and the response will be an termination report.
        """

        try:
            # Empty the process location
            ActiniaInterface.PROCESS_LOCATION = {}
            request_doc = request.get_json()
            g = Graph(graph_description=request_doc)
            result_name, process_list = g.to_actinia_process_list()

            if len(ActiniaInterface.PROCESS_LOCATION) == 0 or len(ActiniaInterface.PROCESS_LOCATION) > 1:
                return make_response(jsonify({"description":"Processes can only be defined for a single location!"},
                                             400))

            location = ActiniaInterface.PROCESS_LOCATION.keys()
            location = list(location)[0]

            process_chain = dict(list=process_list, version="1")

            # pprint.pprint(process_chain)

            status, response = self.iface.async_ephemeral_processing_export(location=location,
                                                                            process_chain=process_chain)
            status, response = self.wait_until_finished(response=response, max_time=1000)

            if status == 200:
                result_url = response["urls"]["resources"]
                if len(result_url) == 1:
                    # attempt to return an image
                    result_data = self.iface.get_resource(result_url[0])
                    if result_url[0][-4:] in ("tiff", ".tif"):
                        mimetype = "image/tiff"
                    else:
                        mimetype = "unknown"

                    return Response(result_data.content,
                                    mimetype=mimetype,
                                    direct_passthrough=True)

                return make_response(jsonify({"job_id":response["resource_id"],
                                              "job_info":response}), status)
            else:
                return ErrorSchema(id="1234567890", code=404,
                                   message=str(response), links=response["urls"]["status"]).as_response(status)
        except Exception:

            e_type, e_value, e_tb = sys.exc_info()
            traceback_model = dict(message=str(e_value),
                                   traceback=traceback.format_tb(e_tb),
                                   type=str(e_type))
            return ErrorSchema(id="1234567890", code=404, message=str(traceback_model)).as_response(404)

    def wait_until_finished(self, response, max_time: int=10):
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

        if "resource_id" not in response:
            raise Exception(f"Internal server error: {str(response)}")
        resource_id = response["resource_id"]
        start_time = time.time()

        while True:
            status, resp_data = self.iface.resource_info(resource_id)

            if isinstance(resp_data, dict) is False or "status" not in resp_data:
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

        return status, resp_data
