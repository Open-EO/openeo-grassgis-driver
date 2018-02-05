# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger
from openeo_core.processes_process_id import ProcessesProcessId, GET_PROCESSES_PROCESS_ID_DOC
from graas_openeo_core_wrapper import processes

# Import the processes to fill the process.PROCESS_DICT with processes
from graas_openeo_core_wrapper.filter_bbox_process import FilterBBoxProcess
from graas_openeo_core_wrapper.filter_daterange_process import FilterDataRangeProcess


class GRaaSProcessesProcessId(ProcessesProcessId):

    @swagger.doc(GET_PROCESSES_PROCESS_ID_DOC)
    def get(self, process_id):

        if process_id not in processes.PROCESS_DICT:
            return make_response(jsonify({"description": "This process does not exists!"}), 400)

        return make_response(jsonify(processes.PROCESS_DICT[process_id]), 200)
