# -*- coding: utf-8 -*-
from openeo_core.processes import Processes, GET_PROCESSES_DOC
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger
from graas_openeo_core_wrapper import process_definitions


class GRaaSProcesses(Processes):

    @swagger.doc(GET_PROCESSES_DOC)
    def get(self):
        return make_response(jsonify(list(process_definitions.PROCESS_DICT.keys())), 200)
