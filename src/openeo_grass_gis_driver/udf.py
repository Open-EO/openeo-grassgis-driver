# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import Resource

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


GET_UDF_EXAMPLE = {
    "R": {
        "udf_types": [
            "reduce_time",
            "reduce_space",
            "apply_pixel"
        ],
        "versions": {
            "3.1.0": {
                "packages": [
                    "Rcpp_0.12.10",
                    "sp_1.2-5",
                    "rmarkdown_1.6"
                ]
            },
            "3.3.3": {
                "packages": [
                    "Rcpp_0.12.10",
                    "sf_0.5-4",
                    "spacetime_1.2-0"
                ]
            }
        }
    }
}


SUPPORTED_UDF = {
    "python": {
        "udf_types": [
            "reduce_time"
        ],
        "versions": {
            "3.6": {
                "packages": [
                    "numpy",
                    "scipy"
                ]
            }
        }
    }
}

GET_UDF_DOC = {
    "summary": "Describes how custom user-defined functions can be exposed to the data and "
               "which languages are supported by the back-end.",
    "tags": ["UDF"],
    "responses": {
        "200": {
            "description": "Description of UDF support",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "description": "A map with language identifiers such as `R` as keys and an object that "
                                   "defines available versions, extension packages, and UDF schemas.",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "udf_types": {
                                "type": "array",
                                "items": None
                            },
                            "versions": {
                                "type": "object",
                                "description": "A map with version identifiers as keys and an object value that "
                                               "specifies which extension packages are available for the "
                                               "particular version.",
                                "additionalProperties": {
                                    "description": "Extension package identifiers that should include their version "
                                                   "number such as `'sf__0.5-4'`",
                                    "properties": {
                                        "packages": {"type": "array", "items": {"type": "string"}}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "examples": {"application/json": GET_UDF_EXAMPLE}
        },
        "401": {"$ref": "#/responses/auth_required"},
        "403": {"$ref": "#/responses/access_denied"},
        "501": {"$ref": "#/responses/not_implemented"},
        "503": {"$ref": "#/responses/unavailable"}
    }
}


class Udf(Resource):
    def get(self):
        return make_response(jsonify(SUPPORTED_UDF), 200)
