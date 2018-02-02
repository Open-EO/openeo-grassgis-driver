# -*- coding: utf-8 -*-
from openeo_core.capabilities import Capabilities
from flask import make_response, jsonify

GRAAS_CAPABILITIES=["/capabilities","/data", "/data/{product_id}"]

class GRaaSCapabilities(Capabilities):
    def get(self, ):
        return make_response(jsonify(GRAAS_CAPABILITIES), 200)
