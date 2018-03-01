# -*- coding: utf-8 -*-
from openeo_core.udf import GET_UDF_DOC
from openeo_core.udf import Udf
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger


SUPPORTED_UDF = {
    "python": {
        "udf_types": [
            "reduce_time"
        ],
        "versions": {
            "2.7": {
                "packages": [
                    "numpy",
                    "scipy"
                ]
            }
        }
    }
}


class GRaaSUdf(Udf):

    @swagger.doc(GET_UDF_DOC)
    def get(self):
        return make_response(jsonify(SUPPORTED_UDF), 200)
