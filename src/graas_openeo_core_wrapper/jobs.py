# -*- coding: utf-8 -*-
import pprint
from openeo_core.jobs import Jobs, POST_JOBS_DOC
from openeo_core.definitions import DataSetListEntry, DataSetInfo
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from flask import make_response, jsonify, request, g
from flask_restful_swagger_2 import swagger
from graas_openeo_core_wrapper.process_definitions import analyse_process_graph


class GRaaSJobs(Jobs):

    def __init__(self):
        self.iface = GRaaSInterface()

    @swagger.doc(POST_JOBS_DOC)
    def post(self, ):

        try:
            status_code, mapsets = self.iface.list_mapsets()
            if status_code != 200:
                return make_response(jsonify({"description":"An internal error occurred "
                                                            "while catching mapsets!"}, 400))

            count = 0
            name = "openeo_mapset"
            new_mapset = "%s_%i"%(name, count)
            while new_mapset in mapsets:
                count += 1
                new_mapset = "%s_%i"%(name, count)

            process_graph = request.get_json()

            # Transform the process graph into a process chain

            result_name, process_list = analyse_process_graph(process_graph)

            process_chain = dict(list=process_list,
                                 version="1")

            pprint.pprint(process_chain)

            status, response = self.iface.async_persistent_processing(mapset=new_mapset,
                                                                      process_chain=process_chain)
            pprint.pprint(response)

            if status == 200:
                return make_response(jsonify({"job_id":response["resource_id"],
                                              "job_info":response}), status)
            else:
                return make_response(jsonify(response), status)
        except Exception as e:
                return make_response(jsonify(str(e)), 500)
