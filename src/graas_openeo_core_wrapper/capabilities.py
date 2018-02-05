# -*- coding: utf-8 -*-
from openeo_core.capabilities import Capabilities, GET_CAPABILITIES_DOC
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger

GRAAS_CAPABILITIES=["/capabilities",
                    "/data",
                    "/data/{product_id}",
                    '/processes',
                    '/processes/{process_id}']


class GRaaSCapabilities(Capabilities):

    @swagger.doc(GET_CAPABILITIES_DOC)
    def get(self, ):
        return make_response(jsonify(GRAAS_CAPABILITIES), 200)
