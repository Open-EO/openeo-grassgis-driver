# -*- coding: utf-8 -*-
import traceback
from uuid import uuid4
import sys
from flask import make_response, jsonify, request
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.process_graph_db import GraphDB
from openeo_grass_gis_driver.job_db import JobDB
from openeo_grass_gis_driver.error_schemas import ErrorSchema
from openeo_grass_gis_driver.jobs import check_job
from openeo_grass_gis_driver.authentication import ResourceBase

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class JobsJobId(ResourceBase):

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

    def patch(self, job_id):
        try:
            """Update a job in the job database"""
            # TODO: Implement user specific database access
            job = request.get_json()
            if job_id in self.job_db:

                if "process_graph" not in job:
                    error = ErrorSchema(id=uuid4(), message="A process graph is required in the job request")
                    return make_response(error.to_json(), 400)

                job_info = check_job(job=job, job_id=job_id)
                self.job_db[job_id] = job_info
                return make_response(job_id, 204)
            else:
                return make_response(ErrorSchema(id="123456678", code=404,
                                                 message=f"job with id {job_id} not found in database.").to_json(), 404)
        except Exception:

            e_type, e_value, e_tb = sys.exc_info()
            traceback_model = dict(message=str(e_value),
                                   traceback=traceback.format_tb(e_tb),
                                   type=str(e_type))
            error = ErrorSchema(id="1234567890", code=2, message=str(traceback_model))
            return make_response(error.to_json(), 400)

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
