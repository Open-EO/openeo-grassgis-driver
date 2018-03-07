# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger
from openeo_core.processes_process_id import ProcessesProcessId, GET_PROCESSES_PROCESS_ID_DOC
from graas_openeo_core_wrapper import process_definitions

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GRaaSProcessesProcessId(ProcessesProcessId):

    @swagger.doc(GET_PROCESSES_PROCESS_ID_DOC)
    def get(self, process_id):

        if process_id not in process_definitions.PROCESS_DESCRIPTION_DICT:
            return make_response(jsonify({"description": "This process does not exists!"}), 400)

        return make_response(jsonify(process_definitions.PROCESS_DESCRIPTION_DICT[process_id]), 200)
