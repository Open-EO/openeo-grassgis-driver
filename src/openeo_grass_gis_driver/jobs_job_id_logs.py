# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from openeo_grass_gis_driver.actinia_processing.config import Config as ActiniaConfig
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.process_graph_db import GraphDB
from openeo_grass_gis_driver.job_db import JobDB
from openeo_grass_gis_driver.actinia_processing.actinia_job_db import ActiniaJobDB
from openeo_grass_gis_driver.authentication import ResourceBase
from openeo_grass_gis_driver.models.schema_base import EoLink
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema
from openeo_grass_gis_driver.models.job_schemas import JobInformation

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


# see also JobsJobIdResults
class JobsJobIdLogs(ResourceBase):

    def __init__(self):
        ResourceBase.__init__(self)
        self.iface = ActiniaInterface()
        # really use ActiniaConfig user + pw ?
        self.iface.set_auth(ActiniaConfig.USER, ActiniaConfig.PASSWORD)
        self.db = GraphDB()
        self.job_db = JobDB()
        self.actinia_job_db = ActiniaJobDB()

    def get(self, job_id):
        """Return information about a single job

        https://api.openeo.org/#operation/debug-job
        """

        if job_id in self.job_db:
            job: JobInformation = self.job_db[job_id]
            job_logs = {'logs': [], 'links': []}

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

                links = []
                if (job.additional_info['urls'] and
                        "resources" in job.additional_info['urls']):
                    resource_links = job.additional_info['urls']['resources']

                    for link in resource_links:
                        eo_link = EoLink(href=link)
                        links.append(eo_link)

                job_logs['logs'] = job
                job_logs['links'] = links

            return make_response(jsonify(job_logs), 200)
        else:
            return ErrorSchema(
                id="123456678",
                code=404,
                message=f"job with id {job_id} not found in database.").as_response(
                http_status=404)
