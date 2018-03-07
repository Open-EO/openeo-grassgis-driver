# -*- coding: utf-8 -*-
import pprint
from openeo_core.jobs import POST_JOBS_DOC
from openeo_core.jobs import Jobs
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from flask import make_response, jsonify, request
from flask_restful_swagger_2 import swagger
from graas_openeo_core_wrapper.graph_db import GraphDB
from graas_openeo_core_wrapper.process_definitions import udf_reduce_time

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


python_udfs = dict(python={})
python_udfs["python"][udf_reduce_time.PROCESS_NAME] = udf_reduce_time.DOC


class GRaaSUdfType(Jobs):

    def __init__(self):
        self.iface = GRaaSInterface()
        self.db = GraphDB()

    @swagger.doc(POST_JOBS_DOC)
    def get(self, lang, udf_type):

        if lang not in python_udfs:
            return make_response(jsonify({"description": "UDF type with specified identifier is not available"}), 404)

        if udf_type not in python_udfs[lang]:
            return make_response(jsonify({"description": "UDF type with specified identifier is not available"}), 404)

        return make_response(jsonify(python_udfs[lang][udf_type]), 200)
