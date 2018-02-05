# -*- coding: utf-8 -*-
from openeo_core.processes import Processes, GET_PROCESSES_DOC
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger

PROCESS_DICT = {}


class GRaaSProcesses(Processes):

    @swagger.doc(GET_PROCESSES_DOC)
    def get(self):

        l = list(PROCESS_DICT.keys())

        return make_response(jsonify(l), 200)
