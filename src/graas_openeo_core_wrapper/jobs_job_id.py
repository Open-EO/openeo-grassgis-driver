# -*- coding: utf-8 -*-
import pprint
from openeo_core.jobs_job_id import JobsJobId, GET_JOBS_ID_DOC
from openeo_core.definitions import DataSetListEntry, DataSetInfo
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from flask import make_response, jsonify, request, g
from flask_restful_swagger_2 import swagger
from graas_openeo_core_wrapper.process_definitions import analyse_process_graph

example = {
    "job_id": "748df7caa8c84a7ff6e",
    "user_id": "bd6f9faf93b4",
    "status": "running",
    "process_graph": {
        "process_id": "filter_daterange",
        "args": [
            {"A": {"product_id": "Sentinel2A-L1C"}},
            {"from": "2017-01-01"},
            {"to": "2017-01-31"}
        ]
    },
    "submitted": "2017-01-01T09:32:12Z",
    "last_update": "2017-01-01T09:36:18Z",
    "consumed_credits": "392"
}


class GRaaSJobsJobId(JobsJobId):

    def __init__(self):
        self.iface = GRaaSInterface()

    @swagger.doc(GET_JOBS_ID_DOC)
    def post(self, resource_id):

        try:
            status, response = self.iface.resource_info(resource_id)
            pprint.pprint(response)

            if status == 200:
                return make_response(jsonify({"job_id":response["resource_id"],
                                              "job_info":response}), status)
            else:
                return make_response(jsonify(response), status)
        except Exception as e:
                return make_response(jsonify(str(e)), 500)
