# -*- coding: utf-8 -*-
from openeo_core.processes import Processes, GET_PROCESSES_DOC
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger
from graas_openeo_core_wrapper import process_definitions

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GRaaSProcesses(Processes):

    @swagger.doc(GET_PROCESSES_DOC)
    def get(self):
        return make_response(jsonify(list(process_definitions.PROCESS_DESCRIPTION_DICT.keys())), 200)
