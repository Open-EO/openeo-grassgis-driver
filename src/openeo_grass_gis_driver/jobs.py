# -*- coding: utf-8 -*-
from uuid import uuid4
from datetime import datetime
from flask_restful import Resource
from flask import make_response, jsonify, request, url_for

from openeo_grass_gis_driver.actinia_processing.config import Config as ActiniaConfig
from openeo_grass_gis_driver.authentication import ResourceBase
from openeo_grass_gis_driver.process_graph_db import GraphDB
from openeo_grass_gis_driver.job_db import JobDB
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph
from openeo_grass_gis_driver.models.job_schemas import JobInformation, JobList
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


OUTPUT_FORMATS = {
  "output": {
    "GTiff": {
      "gis_data_types": [
        "raster"
      ],
      "parameters": {},
      "links": [{
        "href": "https://www.gdal.org/frmt_gtiff.html",
        "rel": "about",
        "title": "GDAL on the GeoTiff file format and storage options"
      }]
    }
  },
  "input": {}
}

class OutputFormats(Resource):
    def get(self, ):
        return make_response(jsonify(OUTPUT_FORMATS), 200)


class Jobs(ResourceBase):
    """The /jobs endpoint implementation"""

    def __init__(self):
        ResourceBase.__init__(self)
        self.iface = ActiniaInterface()
        self.iface.set_auth(ActiniaConfig.USER, ActiniaConfig.PASSWORD)
        self.graph_db = GraphDB()
        self.job_db = JobDB()

    def get(self):
        """Return all jobs in the job database"""
        # TODO: Implement user specific database access

        jobs = []

        for key in self.job_db:
            job = self.job_db[key]
            job.process = None
            jobs.append(job)

        job_list = JobList(jobs=jobs, links = [])
        return job_list.as_response(http_status=200)

    def post(self):
        """Submit a new job to the job database"""
        # TODO: Implement user specific database access

        job_id = f"user-job-{str(uuid4())}"
        # job_id = str(uuid4())
        job = request.get_json()

        if "process" not in job:
            job = {"process": job}
            # return ErrorSchema(id=uuid4(), message="A process graph is required in the request").as_response(400)

        job_info = check_job(job=job, job_id=job_id)
        self.job_db[job_id] = job_info

        response = make_response(job_id, 201)
        # add openeo-identifier
        response.headers["OpenEO-Identifier"] = job_id
        # add location, e.g. "https://openeo.org/api/v1.0/resource/<job_id>"
        response.headers["Location"] = ("%s/%s") % (url_for(".jobs"), job_id)
        
        return response

    def delete(self):
        """Clear the job database"""
        self.job_db.clear()
        return make_response("All jobs has been successfully deleted", 204)


def check_job(job, job_id):
    title = None
    if "title" in job:
        title = job["title"]

    description = None
    if "description" in job:
        description = job["description"]

    process_graph = None
    if "process" in job:
        process_graph = job["process"]["process_graph"]
    else:
        process_graph = job["process_graph"]
    process = ProcessGraph(title=title, description=description, process_graph=process_graph)

    created = str(datetime.now().isoformat())

    job_info = JobInformation(id=job_id, title=title,
                              description=description,
                              process=process, updated=None,
                              created=created, status="created")

    return job_info
