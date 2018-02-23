# -*- coding: utf-8 -*-
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
    def get(self, ):

        dataset_list = []

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

        process_chain = analyse_process_graph(process_graph)

        return make_response(jsonify(dataset_list), 200)
