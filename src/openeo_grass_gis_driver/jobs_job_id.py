# -*- coding: utf-8 -*-
import traceback
from uuid import uuid4
import sys
from flask import make_response, request
from openeo_grass_gis_driver.capabilities import CAPABILITIES
from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
     ActiniaInterface
from openeo_grass_gis_driver.actinia_processing.config import \
     Config as ActiniaConfig
from openeo_grass_gis_driver.process_graph_db import GraphDB
from openeo_grass_gis_driver.job_db import JobDB
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema
from openeo_grass_gis_driver.models.job_schemas import JobInformation
from openeo_grass_gis_driver.jobs import check_job
from openeo_grass_gis_driver.authentication import ResourceBase
from openeo_grass_gis_driver.models.schema_base import EoLink

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class JobsJobId(ResourceBase):

    def __init__(self):
        ResourceBase.__init__(self)
        self.iface = ActiniaInterface()
        self.iface.set_auth(ActiniaConfig.USER, ActiniaConfig.PASSWORD)
        self.db = GraphDB()
        self.job_db = JobDB()

    def get(self, job_id):
        """Return information about a single job

        https://api.openeo.org/#operation/describe-job
        """

        if job_id in self.job_db:
            job: JobInformation = self.job_db[job_id]

            job.stac_version = CAPABILITIES['stac_version']
            job.type = "Feature"
            job.geometry = "json:null"
            job.properties = dict()
            job.properties['datetime'] = None
            job.assets = dict()
            job.links = []

            # Check for the actinia id to get the latest actinia job
            # information
            if job_id in self.actinia_job_db:
                actinia_id = self.actinia_job_db[job_id]
                code, job_info = self.iface.resource_info(
                    resource_id=actinia_id)

                if code == 200:
                    # Add the actinia information to the openeo job
                    if job.additional_info != job_info:
                        job.additional_info = job_info
                        job.updated = job_info["datetime"].replace(
                            " ", "T").replace(
                            "'", "").replace(
                            '"', '')
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

                if (job.additional_info['urls'] and
                        "resources" in job.additional_info['urls']):
                    resource_links = job.additional_info['urls']['resources']

                    if job.links is None:
                        job.links = []

                    for link in resource_links:
                        eo_link = EoLink(href=link)
                        job.links.append(eo_link)

            return job.as_response(http_status=200)
        else:
            return ErrorSchema(
                id="123456678",
                code=404,
                message=f"job with id {job_id} not found in database.").as_response(
                http_status=404)

    def patch(self, job_id):
        try:
            """Update a job in the job database"""
            # TODO: Implement user specific database access
            job = request.get_json()
            if job_id in self.job_db:

                if "process" not in job:
                    return ErrorSchema(
                        id=uuid4(),
                        message="A process is required in the job request").as_response(
                        http_status=400)

                job_info = check_job(job=job, job_id=job_id)
                self.job_db[job_id] = job_info
                return make_response(job_id, 204)
            else:
                return ErrorSchema(
                    id="123456678",
                    code=404,
                    message=f"job with id {job_id} not found in database.").as_response(
                    http_status=404)
        except Exception:

            e_type, e_value, e_tb = sys.exc_info()
            traceback_model = dict(message=str(e_value),
                                   traceback=traceback.format_tb(e_tb),
                                   type=str(e_type))
            return ErrorSchema(
                id="1234567890",
                code=2,
                message=str(traceback_model)).as_response(
                http_status=400)

    def delete(self, job_id):
        """Delete a single job

        https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management/paths/~1jobs~1{job_id}/delete
        """

        if job_id in self.job_db:
            if job_id in self.actinia_job_db:
                actinia_id = self.actinia_job_db[job_id]
                code, job_info = self.iface.delete_resource(
                    resource_id=actinia_id)

            del self.job_db[job_id]
            return make_response("The job has been successfully deleted", 204)
        else:
            return ErrorSchema(
                id="123456678",
                code=404,
                message=f"job with id {job_id} not found in database.").as_response(
                http_status=404)
