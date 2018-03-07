# -*- coding: utf-8 -*-
from openeo_core.capabilities import Capabilities, GET_CAPABILITIES_DOC
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


GRAAS_CAPABILITIES=["/capabilities",
                    "/data",
                    "/data/{product_id}",
                    '/processes',
                    '/processes/{process_id}',
                    '/jobs',
                    '/jobs/job_id',
                    '/udf',
                    '/udf/{lang}/{udf_type}']


class GRaaSCapabilities(Capabilities):

    @swagger.doc(GET_CAPABILITIES_DOC)
    def get(self, ):
        return make_response(jsonify(GRAAS_CAPABILITIES), 200)
