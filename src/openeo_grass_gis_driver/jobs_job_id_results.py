# -*- coding: utf-8 -*-
import sys
import traceback
from datetime import datetime
from flask import make_response, jsonify, request
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.process_graph_db import GraphDB
from openeo_grass_gis_driver.job_db import JobDB
from openeo_grass_gis_driver.actinia_processing.actinia_job_db import ActiniaJobDB
from openeo_grass_gis_driver.error_schemas import ErrorSchema
from openeo_grass_gis_driver.job_schemas import JobInformation
from openeo_grass_gis_driver.actinia_processing.base import analyse_process_graph
from openeo_grass_gis_driver.authentication import ResourceBase

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class JobsJobIdResults(ResourceBase):

    def __init__(self):
        self.iface = ActiniaInterface()
        self.iface.set_auth(request.authorization.username, request.authorization.password)
        self.db = GraphDB()
        self.job_db = JobDB()
        self.actinia_job_db = ActiniaJobDB()

    def get(self, job_id):
        """Return information about a single job

        https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management/paths/~1jobs~1{job_id}/get
        """

        if job_id in self.job_db:
            job: JobInformation = self.job_db[job_id]

            # Check for the actinia id to get the latest actinia job information
            if job_id in self.actinia_job_db:
                actinia_id = self.actinia_job_db[job_id]
                print("Resource id", actinia_id)
                code, job_info = self.iface.resource_info(resource_id=actinia_id)

                if code == 200:
                    # Add the actinia information to the openeo job
                    if job.additional_info != job_info:
                        job.additional_info = job_info
                        job.updated = job_info["datetime"]
                        if job_info["status"] == "finished":
                            job.status = "finished"
                        if job_info["status"] == "error":
                            job.status = "error"
                        if job_info["status"] == "accepted":
                            job.status = "queued"
                        if job_info["status"] == "terminated":
                            job.status = "canceled"
                        if job_info["status"] == "running":
                            job.status = "running"

                        # Store the updated job in the database
                        self.job_db[job_id] = job
                else:
                    if job.additional_info != job_info:
                        job.additional_info = job_info
                        self.job_db[job_id] = job

            return make_response(job.to_json(), 200)
        else:
            return make_response(ErrorSchema(id="123456678", code=404,
                                             message=f"job with id {job_id} not found in database.").to_json(), 404)

    def post(self, job_id):
        """Start a processing job in the actinia backend

        https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management/paths/~1jobs~1{job_id}~1results/post
        """
        try:
            if job_id in self.job_db:
                job: JobInformation = self.job_db[job_id]

                status, response = self.send_actinia_processing_request(job=job)
                self.actinia_job_db[job_id] = response["resource_id"]

                job.additional_info = response
                job.status = "queued"
                job.updated = str(datetime.now())

                self.job_db[job_id] = job

                return make_response("The creation of the resource has been queued successfully.", 202)
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

    def send_actinia_processing_request(self, job: JobInformation):
        try:
            # Empty the process location
            ActiniaInterface.PROCESS_LOCATION = {}
            # Transform the process graph into a process chain and store the input location
            # Check all locations in the process graph
            result_name, process_list = analyse_process_graph({"process_graph":job.process_graph})

            if len(ActiniaInterface.PROCESS_LOCATION) == 0 or len(ActiniaInterface.PROCESS_LOCATION) > 1:
                raise Exception("Processes can only be defined for a single location!")

            location = ActiniaInterface.PROCESS_LOCATION.keys()
            location = list(location)[0]

            process_chain = dict(list=process_list,
                                 version="1")

            # pprint.pprint(process_chain)

            status, response = self.iface.async_ephemeral_processing_export(location=location,
                                                                            process_chain=process_chain)

            return status, response
        except Exception:

            e_type, e_value, e_tb = sys.exc_info()
            traceback_model = dict(message=str(e_value),
                                   traceback=traceback.format_tb(e_tb),
                                   type=str(e_type))
            raise Exception(str(traceback_model))

    def delete(self, job_id):
        """Cancel a running job

        https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management/paths/~1jobs~1{job_id}~1results/delete
        """

        if job_id in self.job_db:

            # Check for the actinia id to get the latest actinia job information
            if job_id in self.actinia_job_db:
                actinia_id = self.actinia_job_db[job_id]
                code, job_info = self.iface.delete_resource(resource_id=actinia_id)

            return make_response("The job has been successfully cancelled", 204)
        else:
            return make_response(ErrorSchema(id="123456678", code=404,
                                             message=f"job with id {job_id} not found in database.").to_json(), 404)
