# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from openeo_grass_gis_driver.actinia_processing.config import \
     Config as ActiniaConfig
from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
     ActiniaInterface
from openeo_grass_gis_driver.process_graph_db import GraphDB
from openeo_grass_gis_driver.job_db import JobDB
from openeo_grass_gis_driver.actinia_processing.actinia_job_db import \
     ActiniaJobDB
from openeo_grass_gis_driver.authentication import ResourceBase
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


# not implemented on actinia
class JobsJobIdEstimate(ResourceBase):

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

        https://api.openeo.org/#operation/estimate-job
        """

        # TODO
        # at least one of costs, duration, size must be specified
        # optional: downloads_included, expires
        if job_id in self.job_db:
            estimate = {"costs": 0
                        }

            return make_response(jsonify(estimate), 200)
        else:
            return ErrorSchema(
                id="123456678",
                code=404,
                message=f"job with id {job_id} not found in database.").as_response(
                http_status=404)
