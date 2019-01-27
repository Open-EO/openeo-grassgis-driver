# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.graph_db import GraphDB
from openeo_grass_gis_driver.job_db import JobDB
from openeo_grass_gis_driver.error_schemas import ErrorSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class JobsJobId(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()
        self.db = GraphDB()
        self.job_db = JobDB()

    def get(self, job_id):
        """Return information about a single job

        https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management/paths/~1jobs~1{job_id}/get
        """

        if job_id in self.job_db:
            job = self.job_db[job_id]
            return make_response(job.to_json(), 200)
        else:
            return make_response(ErrorSchema(id="123456678", code=404,
                                             message=f"job with id {job_id} not found in database.").to_json(), 404)

    def delete(self, job_id):
        """Delete a single job

        https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management/paths/~1jobs~1{job_id}/delete
        """

        if job_id in self.job_db:
            del self.job_db[job_id]
            return make_response("The job has been successfully deleted", 204)
        else:
            return make_response(ErrorSchema(id="123456678", code=404,
                                             message=f"job with id {job_id} not found in database.").to_json(), 404)

    def check_actinia_job(self, job_id):

        try:
            status, response = self.iface.resource_info(job_id)
            if status == 200:
                process_graph = self.db[job_id]

                info = dict(job_id=job_id,
                            user_id=response["user_id"],
                            status=response["status"],
                            process_graph=process_graph,
                            submitted=response["accept_datetime"],
                            last_update=response["datetime"],
                            consumed_credits=response["time_delta"],
                            job_info=response)

                if "urls" in response and "resources" in response["urls"]:
                    info["resources"] = response["urls"]["resources"]

                return make_response(jsonify(info), 200)
            else:
                process_graph = self.db[job_id]
                info = dict(job_id=job_id,
                            status="error",
                            process_graph=process_graph,
                            job_info=response)

                return make_response(jsonify(info), status)
        except Exception as e:
                return make_response(jsonify({"error": str(e)}), 500)

    def delete_actinia_job(self, job_id):

        try:
            status, response = self.iface.resource_info(job_id)

            if status == 200:

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
                if status != 200:
                    process_graph = self.db[job_id]
                    info = dict(job_id=job_id,
                                status="error",
                                process_graph=process_graph,
                                job_info=response)
                return make_response(jsonify(info), status)
            else:
                process_graph = self.db[job_id]
                info = dict(job_id=job_id,
                            status="error",
                            process_graph=process_graph,
                            job_info=response)

                return make_response(jsonify(info), status)
        except Exception as e:
                return make_response(jsonify({"error": str(e)}), 500)
