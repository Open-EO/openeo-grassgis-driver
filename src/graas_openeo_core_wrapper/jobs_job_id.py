# -*- coding: utf-8 -*-
import pprint
from openeo_core.jobs_job_id import GET_JOBS_ID_DOC, DELETE_JOBS_ID_DOC
from openeo_core.jobs_job_id import JobsJobId
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger
from graas_openeo_core_wrapper.graph_db import GraphDB


class GRaaSJobsJobId(JobsJobId):

    def __init__(self):
        self.iface = GRaaSInterface()
        self.db = GraphDB()

    @swagger.doc(GET_JOBS_ID_DOC)
    def get(self, job_id):

        try:
            status, response = self.iface.resource_info(job_id)
            # pprint.pprint(response)

            process_graph = self.db[job_id]

            info = dict(job_id=job_id,
                        user_id=response["user_id"],
                        status=response["status"],
                        process_graph=process_graph,
                        submitted=response["accept_datetime"],
                        last_update=response["datetime"],
                        consumed_credits=response["time_delta"],
                        job_info=response)

            if status == 200:
                return make_response(jsonify(info), 200)
            else:
                return make_response(jsonify(response), status)
        except Exception as e:
                return make_response(jsonify({"error": str(e)}), 500)

    @swagger.doc(DELETE_JOBS_ID_DOC)
    def delete(self, job_id):

        try:
            status, response = self.iface.resource_info(job_id)
            process_graph = self.db[job_id]

            info = dict(job_id=job_id,
                        user_id="scheduled",
                        status="submitted",
                        process_graph=process_graph,
                        submitted=response["accept_datetime"],
                        last_update=response["datetime"],
                        consumed_credits=response["time_delta"],
                        job_info=response)

            status, response = self.iface.delete_resource(job_id)
            #pprint.pprint(response)

            if status == 200:
                return make_response(jsonify(info), 200)
            else:
                return make_response(jsonify(response), status)
        except Exception as e:
                return make_response(jsonify({"error": str(e)}), 500)
